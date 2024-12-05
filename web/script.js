const taskInput = document.getElementById("task-input");
const addTaskBtn = document.getElementById("add-task-btn");
const taskList = document.getElementById("task-list");

addTaskBtn.addEventListener("click", function () {
    const taskText = taskInput.value.trim();
    if (taskText === "") {
        alert("Please enter a task!");
        return;
    }

    const newTask = document.createElement("li");
    newTask.textContent = taskText;
    taskList.appendChild(newTask);
    taskInput.value = "";

    newTask.addEventListener("click", function () {
        taskList.removeChild(newTask);
    });
});
