#pragma once

/* MACRO_FUNCS_BEGIN */
#define configUSE_PREEMPTION		1
#define configUSE_IDLE_HOOK		0
#define configUSE_TICK_HOOK		0
#define configCPU_CLOCK_HZ		( ( unsigned long ) 64000000 )
#define configTICK_RATE_HZ		( ( TickType_t ) 10 )
#define configMAX_PRIORITIES		( 5 )
#define configMINIMAL_STACK_SIZE	( ( unsigned short ) 128 )
#define configTOTAL_HEAP_SIZE		( ( size_t ) ( 17 * 1024 ) )
#define configMAX_TASK_NAME_LEN		( 16 )
#define configUSE_TRACE_FACILITY	0
#define configUSE_16_BIT_TICKS		0
#define configIDLE_SHOULD_YIELD		1

#define configUSE_CO_ROUTINES 		0
#define configMAX_CO_ROUTINE_PRIORITIES ( 2 )
#define configUNIQUE_INTERRUPT_PRIORITIES ( 16 )
#define configTOTAL_MPU_REGIONS         (8)

#define configUSE_TIMERS                1
#define configTIMER_TASK_PRIORITY       2
#define configTIMER_QUEUE_LENGTH        6
#define configTIMER_TASK_STACK_DEPTH    (128)

#define INCLUDE_vTaskPrioritySet	1
#define INCLUDE_uxTaskPriorityGet	1
#define INCLUDE_vTaskDelete		1
#define INCLUDE_vTaskCleanUpResources	0
#define INCLUDE_vTaskSuspend		1
#define INCLUDE_vTaskDelayUntil		1
#define INCLUDE_vTaskDelay		1
#define configKERNEL_INTERRUPT_PRIORITY	255

#define configMAX_SYSCALL_INTERRUPT_PRIORITY	191

/* Interrupt vector */
#define vPortSVCHandler Py_SVC_Handler
#define xPortPendSVHandler Py_PendSV_Handler
#define xPortSysTickHandler Py_SysTick_Handler
#define configLIBRARY_KERNEL_INTERRUPT_PRIORITY	15

/* MACRO_FUNCS_END */
