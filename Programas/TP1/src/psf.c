#include "arm_math.h"
#include "sapi.h"

#define SCT_PWM_PIN_LED 2
#define SCT_PWM_LED 2
#define SCT_ADC_PIN_OUT 8
#define SCT_ADC_OUT 1
#define ADC_FRAME_SAMPLES 128
#define ADC_TIGGER_VALUE 512
#define ADC_SAMPLE_RATE 10000
#define ADC_BITS 10

struct header_struct {
    char pre[8];
    uint32_t id;
    uint16_t N;
    uint16_t fs;
    uint32_t maxIndex;
    uint32_t minIndex;
    q15_t maxValue;
    q15_t minValue;
    q15_t rms;
    char pos[4];
} __attribute__((packed)) header = {
    "*header*", 0, ADC_FRAME_SAMPLES, ADC_SAMPLE_RATE, 0, 0, 0, 0, 0, "end*"};

int16_t adc[ADC_FRAME_SAMPLES];
volatile uint16_t index;

void ADC0_IRQHandler(void) {
    static enum {
        ESPERANDO_MENOR,
        ESPERANDO_MAYOR,
        MUESTREANDO,
    } estado = ESPERANDO_MENOR;
    uint16_t sample;

    Chip_ADC_ReadValue(LPC_ADC0, ADC_CH1, &sample);

    if (index == 0) {
        if (estado == MUESTREANDO) estado = ESPERANDO_MENOR;
        switch (estado) {
            case ESPERANDO_MENOR:
                if (sample < ADC_TIGGER_VALUE) estado = ESPERANDO_MAYOR;
                break;
            case ESPERANDO_MAYOR:
                if (sample > ADC_TIGGER_VALUE) estado = MUESTREANDO;
                break;
            default:
                break;
        }
    }
    if (estado == MUESTREANDO) {
        adc[index] = (((sample - 512)) >> (10 - ADC_BITS)) << (6 + (10 - ADC_BITS));
        index++;
    }
    gpioToggle(LED1);  // este led blinkea a fs/2
}

void adc_init(void) {
    ADC_CLOCK_SETUP_T adc;

    Chip_ADC_Init(LPC_ADC0, &adc);
    Chip_ADC_EnableChannel(LPC_ADC0, ADC_CH1, ENABLE);

    Chip_ADC_SetStartMode(LPC_ADC0, ADC_START_ON_CTOUT8, ADC_TRIGGERMODE_FALLING);
    NVIC_EnableIRQ(ADC0_IRQn);
}

void sct_init(void) {
    uint16_t dutty = Chip_SCTPWM_GetTicksPerCycle(LPC_SCT) / 2;

    Chip_SCTPWM_Init(LPC_SCT);
    Chip_SCTPWM_SetRate(LPC_SCT, ADC_SAMPLE_RATE);

    Chip_SCTPWM_SetOutPin(LPC_SCT, SCT_ADC_OUT, SCT_ADC_PIN_OUT);
    Chip_SCTPWM_SetDutyCycle(LPC_SCT, SCT_ADC_OUT, dutty);

    Chip_SCTPWM_Start(LPC_SCT);
}

int main(void) {
    boardConfig();
    uartConfig(UART_USB, 460800);

    adc_init();
    sct_init();

    while (1) {
        index = 0;
        Chip_ADC_Int_SetChannelCmd(LPC_ADC0, ADC_CH1, ENABLE);
        while (index < header.N) {
            __WFI();
        };
        Chip_ADC_Int_SetChannelCmd(LPC_ADC0, ADC_CH1, DISABLE);

        gpioToggle(LED2);
        arm_max_q15(adc, header.N, &header.maxValue, &header.maxIndex);
        arm_min_q15(adc, header.N, &header.minValue, &header.minIndex);
        arm_rms_q15(adc, header.N, &header.rms);
        header.id++;
        uartWriteByteArray(UART_USB, (uint8_t *)&header, sizeof(header));
        uartWriteByteArray(UART_USB, (uint8_t *)adc, sizeof(adc));
    }
}
