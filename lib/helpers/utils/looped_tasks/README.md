# looped tasks

Solution for defining and executing asynchronously and continuously (in endless loops) given tasks which can be dependent on each other.

User defines tasks - objects storing some given method - and assigns unique names for them. 
User defines <i>HpLoopedTaskManager</i> object, registers the tasks mentioned above to it and defines its dependencies:  
* some tasks can execute when other tasks have its last execution successful 
* some tasks can execute when other tasks have finished their first execution

 <i>HpLoopedTaskManager</i> object provides feature of notifying about current statuses of its tasks - using callback mechanism.