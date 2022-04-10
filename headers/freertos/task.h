#pragma once
#define INC_TASK_H

/* INCLUDE_BEGIN */
#ifndef INC_FREERTOS_H
    #error "include FreeRTOS.h must appear in source files before include task.h"
#endif

#include "list.h"
/* INCLUDE_END */

/* STRUCT_BEGIN */
struct tskTaskControlBlock;
typedef struct tskTaskControlBlock * TaskHandle_t;

typedef BaseType_t (* TaskHookFunction_t)( void * );

typedef enum
{
    eRunning = 0, /* A task is querying the state of itself, so must be running. */
    eReady,       /* The task being queried is in a ready or pending ready list. */
    eBlocked,     /* The task being queried is in the Blocked state. */
    eSuspended,   /* The task being queried is in the Suspended state, or is in the Blocked state with an infinite time out. */
    eDeleted,     /* The task being queried has been deleted, but its TCB has not yet been freed. */
    eInvalid      /* Used as an 'invalid state' value. */
} eTaskState;

typedef enum
{
    eNoAction = 0,            /* Notify the task without updating its notify value. */
    eSetBits,                 /* Set bits in the task's notification value. */
    eIncrement,               /* Increment the task's notification value. */
    eSetValueWithOverwrite,   /* Set the task's notification value to a specific value even if the previous value has not yet been read by the task. */
    eSetValueWithoutOverwrite /* Set the task's notification value if the previous value has been read by the task. */
} eNotifyAction;

typedef struct xTIME_OUT
{
    BaseType_t xOverflowCount;
    TickType_t xTimeOnEntering;
} TimeOut_t;

typedef struct xMEMORY_REGION
{
    void * pvBaseAddress;
    uint32_t ulLengthInBytes;
    uint32_t ulParameters;
} MemoryRegion_t;


typedef struct xTASK_PARAMETERS
{
    TaskFunction_t pvTaskCode;
    const char * pcName; /*lint !e971 Unqualified char types are allowed for strings and single characters only. */
    configSTACK_DEPTH_TYPE usStackDepth;
    void * pvParameters;
    UBaseType_t uxPriority;
    StackType_t * puxStackBuffer;
    MemoryRegion_t xRegions[ portNUM_CONFIGURABLE_REGIONS ];
    #if ( ( portUSING_MPU_WRAPPERS == 1 ) && ( configSUPPORT_STATIC_ALLOCATION == 1 ) )
        StaticTask_t * const pxTaskBuffer;
    #endif
} TaskParameters_t;

typedef struct xTASK_STATUS
{
    TaskHandle_t xHandle;                         /* The handle of the task to which the rest of the information in the structure relates. */
    const char * pcTaskName;                      /* A pointer to the task's name.  This value will be invalid if the task was deleted since the structure was populated! */ /*lint !e971 Unqualified char types are allowed for strings and single characters only. */
    UBaseType_t xTaskNumber;                      /* A number unique to the task. */
    eTaskState eCurrentState;                     /* The state in which the task existed when the structure was populated. */
    UBaseType_t uxCurrentPriority;                /* The priority at which the task was running (may be inherited) when the structure was populated. */
    UBaseType_t uxBasePriority;                   /* The priority to which the task will return if the task's current priority has been inherited to avoid unbounded priority inversion when obtaining a mutex.  Only valid if configUSE_MUTEXES is defined as 1 in FreeRTOSConfig.h. */
    configRUN_TIME_COUNTER_TYPE ulRunTimeCounter; /* The total run time allocated to the task so far, as defined by the run time stats clock.  See https://www.FreeRTOS.org/rtos-run-time-stats.html.  Only valid when configGENERATE_RUN_TIME_STATS is defined as 1 in FreeRTOSConfig.h. */
    StackType_t * pxStackBase;                    /* Points to the lowest address of the task's stack area. */
    #if ( ( portSTACK_GROWTH > 0 ) && ( configRECORD_STACK_HIGH_ADDRESS == 1 ) )
        StackType_t * pxTopOfStack;               /* Points to the top address of the task's stack area. */
        StackType_t * pxEndOfStack;               /* Points to the end address of the task's stack area. */
    #endif
    configSTACK_DEPTH_TYPE usStackHighWaterMark;  /* The minimum amount of stack space that has remained for the task since the task was created.  The closer this value is to zero the closer the task has come to overflowing its stack. */
} TaskStatus_t;

typedef enum
{
    eAbortSleep = 0,           /* A task has been made ready or a context switch pended since portSUPPRESS_TICKS_AND_SLEEP() was called - abort entering a sleep mode. */
    eStandardSleep,            /* Enter a sleep mode that will not last any longer than the expected idle time. */
    #if ( INCLUDE_vTaskSuspend == 1 )
        eNoTasksWaitingTimeout /* No tasks are waiting for a timeout so it is safe to enter a sleep mode that can only be exited by an external interrupt. */
    #endif /* INCLUDE_vTaskSuspend */
} eSleepModeStatus;
/* STRUCT_END */

/* MACRO_FUNC_BEGIN */
#define tskKERNEL_VERSION_NUMBER       "V10.4.4+"
#define tskKERNEL_VERSION_MAJOR        10
#define tskKERNEL_VERSION_MINOR        4
#define tskKERNEL_VERSION_BUILD        4

/* MPU region parameters passed in ulParameters
 * of MemoryRegion_t struct. */
#define tskMPU_REGION_READ_ONLY        ( 1UL << 0UL )
#define tskMPU_REGION_READ_WRITE       ( 1UL << 1UL )
#define tskMPU_REGION_EXECUTE_NEVER    ( 1UL << 2UL )
#define tskMPU_REGION_NORMAL_MEMORY    ( 1UL << 3UL )
#define tskMPU_REGION_DEVICE_MEMORY    ( 1UL << 4UL )

#define tskDEFAULT_INDEX_TO_NOTIFY     ( 0 )



#define tskIDLE_PRIORITY    ( ( UBaseType_t ) 0U )

#define taskYIELD()                        portYIELD()

#define taskENTER_CRITICAL()               portENTER_CRITICAL()
#define taskENTER_CRITICAL_FROM_ISR()      portSET_INTERRUPT_MASK_FROM_ISR()

#define taskEXIT_CRITICAL()                portEXIT_CRITICAL()
#define taskEXIT_CRITICAL_FROM_ISR( x )    portCLEAR_INTERRUPT_MASK_FROM_ISR( x )

#define taskDISABLE_INTERRUPTS()           portDISABLE_INTERRUPTS()


#define taskENABLE_INTERRUPTS()            portENABLE_INTERRUPTS()

#define taskSCHEDULER_SUSPENDED      ( ( BaseType_t ) 0 )
#define taskSCHEDULER_NOT_STARTED    ( ( BaseType_t ) 1 )
#define taskSCHEDULER_RUNNING        ( ( BaseType_t ) 2 )

#define vTaskDelayUntil( pxPreviousWakeTime, xTimeIncrement )           \
    {                                                                   \
        ( void ) xTaskDelayUntil( pxPreviousWakeTime, xTimeIncrement ); \
    }

#define xTaskNotify( xTaskToNotify, ulValue, eAction ) \
    xTaskGenericNotify( ( xTaskToNotify ), ( tskDEFAULT_INDEX_TO_NOTIFY ), ( ulValue ), ( eAction ), NULL )
#define xTaskNotifyIndexed( xTaskToNotify, uxIndexToNotify, ulValue, eAction ) \
    xTaskGenericNotify( ( xTaskToNotify ), ( uxIndexToNotify ), ( ulValue ), ( eAction ), NULL )

#define xTaskNotifyAndQuery( xTaskToNotify, ulValue, eAction, pulPreviousNotifyValue ) \
    xTaskGenericNotify( ( xTaskToNotify ), ( tskDEFAULT_INDEX_TO_NOTIFY ), ( ulValue ), ( eAction ), ( pulPreviousNotifyValue ) )
#define xTaskNotifyAndQueryIndexed( xTaskToNotify, uxIndexToNotify, ulValue, eAction, pulPreviousNotifyValue ) \
    xTaskGenericNotify( ( xTaskToNotify ), ( uxIndexToNotify ), ( ulValue ), ( eAction ), ( pulPreviousNotifyValue ) )

#define xTaskNotifyFromISR( xTaskToNotify, ulValue, eAction, pxHigherPriorityTaskWoken ) \
    xTaskGenericNotifyFromISR( ( xTaskToNotify ), ( tskDEFAULT_INDEX_TO_NOTIFY ), ( ulValue ), ( eAction ), NULL, ( pxHigherPriorityTaskWoken ) )
#define xTaskNotifyIndexedFromISR( xTaskToNotify, uxIndexToNotify, ulValue, eAction, pxHigherPriorityTaskWoken ) \
    xTaskGenericNotifyFromISR( ( xTaskToNotify ), ( uxIndexToNotify ), ( ulValue ), ( eAction ), NULL, ( pxHigherPriorityTaskWoken ) )

#define xTaskNotifyAndQueryIndexedFromISR( xTaskToNotify, uxIndexToNotify, ulValue, eAction, pulPreviousNotificationValue, pxHigherPriorityTaskWoken ) \
    xTaskGenericNotifyFromISR( ( xTaskToNotify ), ( uxIndexToNotify ), ( ulValue ), ( eAction ), ( pulPreviousNotificationValue ), ( pxHigherPriorityTaskWoken ) )
#define xTaskNotifyAndQueryFromISR( xTaskToNotify, ulValue, eAction, pulPreviousNotificationValue, pxHigherPriorityTaskWoken ) \
    xTaskGenericNotifyFromISR( ( xTaskToNotify ), ( tskDEFAULT_INDEX_TO_NOTIFY ), ( ulValue ), ( eAction ), ( pulPreviousNotificationValue ), ( pxHigherPriorityTaskWoken ) )

#define xTaskNotifyWait( ulBitsToClearOnEntry, ulBitsToClearOnExit, pulNotificationValue, xTicksToWait ) \
    xTaskGenericNotifyWait( tskDEFAULT_INDEX_TO_NOTIFY, ( ulBitsToClearOnEntry ), ( ulBitsToClearOnExit ), ( pulNotificationValue ), ( xTicksToWait ) )
#define xTaskNotifyWaitIndexed( uxIndexToWaitOn, ulBitsToClearOnEntry, ulBitsToClearOnExit, pulNotificationValue, xTicksToWait ) \
    xTaskGenericNotifyWait( ( uxIndexToWaitOn ), ( ulBitsToClearOnEntry ), ( ulBitsToClearOnExit ), ( pulNotificationValue ), ( xTicksToWait ) )

#define xTaskNotifyGive( xTaskToNotify ) \
    xTaskGenericNotify( ( xTaskToNotify ), ( tskDEFAULT_INDEX_TO_NOTIFY ), ( 0 ), eIncrement, NULL )
#define xTaskNotifyGiveIndexed( xTaskToNotify, uxIndexToNotify ) \
    xTaskGenericNotify( ( xTaskToNotify ), ( uxIndexToNotify ), ( 0 ), eIncrement, NULL )

#define vTaskNotifyGiveFromISR( xTaskToNotify, pxHigherPriorityTaskWoken ) \
    vTaskGenericNotifyGiveFromISR( ( xTaskToNotify ), ( tskDEFAULT_INDEX_TO_NOTIFY ), ( pxHigherPriorityTaskWoken ) );
#define vTaskNotifyGiveIndexedFromISR( xTaskToNotify, uxIndexToNotify, pxHigherPriorityTaskWoken ) \
    vTaskGenericNotifyGiveFromISR( ( xTaskToNotify ), ( uxIndexToNotify ), ( pxHigherPriorityTaskWoken ) );

#define ulTaskNotifyTake( xClearCountOnExit, xTicksToWait ) \
    ulTaskGenericNotifyTake( ( tskDEFAULT_INDEX_TO_NOTIFY ), ( xClearCountOnExit ), ( xTicksToWait ) )
#define ulTaskNotifyTakeIndexed( uxIndexToWaitOn, xClearCountOnExit, xTicksToWait ) \
    ulTaskGenericNotifyTake( ( uxIndexToWaitOn ), ( xClearCountOnExit ), ( xTicksToWait ) )

#define xTaskNotifyStateClear( xTask ) \
    xTaskGenericNotifyStateClear( ( xTask ), ( tskDEFAULT_INDEX_TO_NOTIFY ) )
#define xTaskNotifyStateClearIndexed( xTask, uxIndexToClear ) \
    xTaskGenericNotifyStateClear( ( xTask ), ( uxIndexToClear ) )

#define ulTaskNotifyValueClear( xTask, ulBitsToClear ) \
    ulTaskGenericNotifyValueClear( ( xTask ), ( tskDEFAULT_INDEX_TO_NOTIFY ), ( ulBitsToClear ) )
#define ulTaskNotifyValueClearIndexed( xTask, uxIndexToClear, ulBitsToClear ) \
    ulTaskGenericNotifyValueClear( ( xTask ), ( uxIndexToClear ), ( ulBitsToClear ) )
/* MACRO_FUNC_END */

/* CODE_BEGIN */
BaseType_t xTaskCreate (TaskFunction_t pxTaskCode,const char * const pcName,const configSTACK_DEPTH_TYPE usStackDepth,void * const pvParameters,UBaseType_t uxPriority,TaskHandle_t * const pxCreatedTask);
TaskHandle_t xTaskCreateStatic (TaskFunction_t pxTaskCode,const char * const pcName,const uint32_t ulStackDepth,void * const pvParameters,UBaseType_t uxPriority,StackType_t * const puxStackBuffer,StaticTask_t * const pxTaskBuffer);
BaseType_t xTaskCreateRestricted (const TaskParameters_t * const pxTaskDefinition,TaskHandle_t * pxCreatedTask);
BaseType_t xTaskCreateRestrictedStatic (const TaskParameters_t * const pxTaskDefinition,TaskHandle_t * pxCreatedTask);
void vTaskAllocateMPURegions (TaskHandle_t xTask,const MemoryRegion_t * const pxRegions);
void vTaskDelete (TaskHandle_t xTaskToDelete);
void vTaskDelay (const TickType_t xTicksToDelay);
BaseType_t xTaskDelayUntil (TickType_t * const pxPreviousWakeTime,const TickType_t xTimeIncrement);
BaseType_t xTaskAbortDelay (TaskHandle_t xTask);
UBaseType_t uxTaskPriorityGet (const TaskHandle_t xTask);
UBaseType_t uxTaskPriorityGetFromISR (const TaskHandle_t xTask);
eTaskState eTaskGetState (TaskHandle_t xTask);
void vTaskGetInfo (TaskHandle_t xTask,TaskStatus_t * pxTaskStatus,BaseType_t xGetFreeStackSpace,eTaskState eState);
void vTaskPrioritySet (TaskHandle_t xTask,UBaseType_t uxNewPriority);
void vTaskSuspend (TaskHandle_t xTaskToSuspend);
void vTaskResume (TaskHandle_t xTaskToResume);
BaseType_t xTaskResumeFromISR (TaskHandle_t xTaskToResume);
void vTaskStartScheduler (void);
void vTaskEndScheduler (void);
void vTaskSuspendAll (void);
BaseType_t xTaskResumeAll (void);
TickType_t xTaskGetTickCount (void);
TickType_t xTaskGetTickCountFromISR (void);
UBaseType_t uxTaskGetNumberOfTasks (void);
char * pcTaskGetName (TaskHandle_t xTaskToQuery);
TaskHandle_t xTaskGetHandle (const char * pcNameToQuery);
UBaseType_t uxTaskGetStackHighWaterMark (TaskHandle_t xTask);
configSTACK_DEPTH_TYPE uxTaskGetStackHighWaterMark2 (TaskHandle_t xTask);
void vTaskSetApplicationTaskTag (TaskHandle_t xTask,TaskHookFunction_t pxHookFunction);
TaskHookFunction_t xTaskGetApplicationTaskTag (TaskHandle_t xTask);
TaskHookFunction_t xTaskGetApplicationTaskTagFromISR (TaskHandle_t xTask);
void vTaskSetThreadLocalStoragePointer (TaskHandle_t xTaskToSet,BaseType_t xIndex,void * pvValue);
void * pvTaskGetThreadLocalStoragePointer (TaskHandle_t xTaskToQuery,BaseType_t xIndex);
void vApplicationStackOverflowHook (TaskHandle_t xTask,char * pcTaskName);
void vApplicationTickHook (void);
void vApplicationGetIdleTaskMemory (StaticTask_t ** ppxIdleTaskTCBBuffer,StackType_t ** ppxIdleTaskStackBuffer,uint32_t * pulIdleTaskStackSize);
BaseType_t xTaskCallApplicationTaskHook (TaskHandle_t xTask,void * pvParameter);
TaskHandle_t xTaskGetIdleTaskHandle (void);
UBaseType_t uxTaskGetSystemState (TaskStatus_t * const pxTaskStatusArray,const UBaseType_t uxArraySize,configRUN_TIME_COUNTER_TYPE * const pulTotalRunTime);
void vTaskList (char * pcWriteBuffer);
void vTaskGetRunTimeStats (char * pcWriteBuffer);
configRUN_TIME_COUNTER_TYPE ulTaskGetIdleRunTimeCounter (void);
configRUN_TIME_COUNTER_TYPE ulTaskGetIdleRunTimePercent (void);
BaseType_t xTaskGenericNotify (TaskHandle_t xTaskToNotify,UBaseType_t uxIndexToNotify,uint32_t ulValue,eNotifyAction eAction,uint32_t * pulPreviousNotificationValue);
BaseType_t xTaskGenericNotifyFromISR (TaskHandle_t xTaskToNotify,UBaseType_t uxIndexToNotify,uint32_t ulValue,eNotifyAction eAction,uint32_t * pulPreviousNotificationValue,BaseType_t * pxHigherPriorityTaskWoken);
BaseType_t xTaskGenericNotifyWait (UBaseType_t uxIndexToWaitOn,uint32_t ulBitsToClearOnEntry,uint32_t ulBitsToClearOnExit,uint32_t * pulNotificationValue,TickType_t xTicksToWait);
void vTaskGenericNotifyGiveFromISR (TaskHandle_t xTaskToNotify,UBaseType_t uxIndexToNotify,BaseType_t * pxHigherPriorityTaskWoken);
uint32_t ulTaskGenericNotifyTake (UBaseType_t uxIndexToWaitOn,BaseType_t xClearCountOnExit,TickType_t xTicksToWait);
BaseType_t xTaskGenericNotifyStateClear (TaskHandle_t xTask,UBaseType_t uxIndexToClear);
uint32_t ulTaskGenericNotifyValueClear (TaskHandle_t xTask,UBaseType_t uxIndexToClear,uint32_t ulBitsToClear);
void vTaskSetTimeOutState (TimeOut_t * const pxTimeOut);
BaseType_t xTaskCheckForTimeOut (TimeOut_t * const pxTimeOut,TickType_t * const pxTicksToWait);
BaseType_t xTaskCatchUpTicks (TickType_t xTicksToCatchUp);
BaseType_t xTaskIncrementTick (void);
void vTaskPlaceOnEventList (List_t * const pxEventList,const TickType_t xTicksToWait);
void vTaskPlaceOnUnorderedEventList (List_t * pxEventList,const TickType_t xItemValue,const TickType_t xTicksToWait);
void vTaskPlaceOnEventListRestricted (List_t * const pxEventList,TickType_t xTicksToWait,const BaseType_t xWaitIndefinitely);
BaseType_t xTaskRemoveFromEventList (const List_t * const pxEventList);
void vTaskRemoveFromUnorderedEventList (ListItem_t * pxEventListItem,const TickType_t xItemValue);
portDONT_DISCARD void vTaskSwitchContext (void);
TickType_t uxTaskResetEventItemValue (void);
TaskHandle_t xTaskGetCurrentTaskHandle (void);
void vTaskMissedYield (void);
BaseType_t xTaskGetSchedulerState (void);
BaseType_t xTaskPriorityInherit (TaskHandle_t const pxMutexHolder);
BaseType_t xTaskPriorityDisinherit (TaskHandle_t const pxMutexHolder);
void vTaskPriorityDisinheritAfterTimeout (TaskHandle_t const pxMutexHolder,UBaseType_t uxHighestPriorityWaitingTask);
UBaseType_t uxTaskGetTaskNumber (TaskHandle_t xTask);
void vTaskSetTaskNumber (TaskHandle_t xTask,const UBaseType_t uxHandle);
void vTaskStepTick (TickType_t xTicksToJump);
eSleepModeStatus eTaskConfirmSleepModeStatus (void);
TaskHandle_t pvTaskIncrementMutexHeldCount (void);
void vTaskInternalSetTimeOutState (TimeOut_t * const pxTimeOut);
/* CODE_END */
