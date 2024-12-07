const taskInput = document.getElementById("task-input");
const addTaskBtn = document.getElementById("add-task-btn");
const taskList = document.getElementById("task-list");

if (document.body.id === "todo") {
    addTaskBtn.addEventListener("click", function () {
        const taskText = taskInput.value.trim();
        if (taskText === "") {
            alert("Prosím přidejte úkol");
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
}

function Ahoj() {
    console.log("Co to tady děláš????");
}
Ahoj();
