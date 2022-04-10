#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
//#include "freertos/system/system.h"

void vHelloWorld(void *pvParams)
{
	for (int i = 0; i < 10; i++) {
		printf("HelloWorld! %d\n", i);
		vTaskDelay(pdMS_TO_TICKS(1000));
	}
	printf("Restart\n");
}

void app_main()
{
	printf("Start\n");
	xTaskCreate(vHelloWorld, "HelloWorld", configMINIMAL_STACK_SIZE * 2, NULL, tskIDLE_PRIORITY, NULL);
}

/*-----------------------------------------------------------*/
extern void esp_vApplicationTickHook();
void vApplicationTickHook()
{
	printf("tick\n");
}

extern void esp_vApplicationIdleHook();
void vApplicationIdleHook()
{
	printf("Idling\n");
}

void vApplicationDaemonTaskStartupHook()
{
	printf("Startup hook\n");
}

/*-----------------------------------------------------------*/

/* configUSE_STATIC_ALLOCATION is set to 1, so the application must provide an
 * implementation of vApplicationGetIdleTaskMemory() to provide the memory that is
 * used by the Idle task. */
void vApplicationGetIdleTaskMemory(StaticTask_t **ppxIdleTaskTCBBuffer,
				   StackType_t **ppxIdleTaskStackBuffer,
				   uint32_t *pulIdleTaskStackSize)
{
	static StaticTask_t xIdleTaskTCB;
	static StackType_t uxIdleTaskStack[configMINIMAL_STACK_SIZE];
	*ppxIdleTaskTCBBuffer = &xIdleTaskTCB;
	*ppxIdleTaskStackBuffer = uxIdleTaskStack;
	*pulIdleTaskStackSize = configMINIMAL_STACK_SIZE;
}
/*-----------------------------------------------------------*/

/**
 * @brief This is to provide the memory that is used by the RTOS daemon/time task.
 *
 * If configUSE_STATIC_ALLOCATION is set to 1, so the application must provide an
 * implementation of vApplicationGetTimerTaskMemory() to provide the memory that is
 * used by the RTOS daemon/time task.
 */
void vApplicationGetTimerTaskMemory(StaticTask_t **ppxTimerTaskTCBBuffer,
					StackType_t **ppxTimerTaskStackBuffer,
					uint32_t *pulTimerTaskStackSize)
{
	static StaticTask_t xTimerTaskTCB;
	static StackType_t uxTimerTaskStack[configTIMER_TASK_STACK_DEPTH];

	*ppxTimerTaskTCBBuffer = &xTimerTaskTCB;
	*ppxTimerTaskStackBuffer = uxTimerTaskStack;
	*pulTimerTaskStackSize = configTIMER_TASK_STACK_DEPTH;
}
