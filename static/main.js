// Create User
document.getElementById("createUserForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;

  const response = await fetch("/user", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, email }),
  });
  const data = await response.json();
  alert(data.message || data.error);
});

// Create Category
document.getElementById("createCategoryForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const name = document.getElementById("categoryName").value;

  const response = await fetch("/categories", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });
  const data = await response.json();
  alert(data.message || data.error);
});

// Create Task
document.getElementById("createTaskForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const title = document.getElementById("taskTitle").value;
  const description = document.getElementById("taskDescription").value;
  const user_id = document.getElementById("assignedUserId").value;
  const priority = document.getElementById("taskPriority").value;
  const due_date = document.getElementById("taskDueDate").value || null;
  const category_id = document.getElementById("taskCategoryId").value || null;

  const response = await fetch("/task", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, description, user_id, priority, due_date, category_id }),
  });
  const data = await response.json();
  alert(data.message || data.error);
});

// Load All Tasks
document.getElementById("loadAllTasks").addEventListener("click", async () => {
  const response = await fetch("/tasks");
  const tasks = await response.json();

  const taskList = document.getElementById("taskList");
  taskList.innerHTML = "";

  tasks.forEach((task) => {
    const listItem = document.createElement("li");
    listItem.innerHTML = `
      <strong>${task.title}</strong><br>
      Description: ${task.description} <br>
      Due Date: ${task.due_date || "None"} - Priority: ${task.priority || "None"} <br>
      Assigned to User: ${task.user_id || "None"}, Category: ${task.category_id || "None"} <br>
      <div class="task-actions">
        <button onclick="markComplete(${task.id}, ${task.is_complete})">${task.is_complete ? "Unmark" : "Mark"} Complete</button>
        <button onclick="deleteTask(${task.id})">Delete</button>
      </div>
    `;
    taskList.appendChild(listItem);
  });
});

// Delete Task
async function deleteTask(taskId) {
  const response = await fetch(`/task/${taskId}`, { method: "DELETE" });
  const data = await response.json();
  alert(data.message || data.error);
  document.getElementById("loadAllTasks").click(); // Reload tasks
}

// Update Task: Mark Complete/Incomplete
async function markComplete(taskId, isComplete) {
  const response = await fetch(`/task/${taskId}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ is_complete: !isComplete }),
  });
  const data = await response.json();
  alert(data.message || data.error);
  document.getElementById("loadAllTasks").click(); // Reload tasks
}

// Filter Tasks
document.getElementById("filterTaskForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const user_id = document.getElementById("filterUserId").value || null;
  const category_id = document.getElementById("filterCategoryId").value || null;
  const due_date = document.getElementById("filterDueDate").value || null;

  let url = `/tasks?`;
  if (user_id) url += `user_id=${user_id}&`;
  if (category_id) url += `category_id=${category_id}&`;
  if (due_date) url += `due_date=${due_date}`;

  const response = await fetch(url);
  const tasks = await response.json();

  const taskList = document.getElementById("taskList");
  taskList.innerHTML = "";

  tasks.forEach((task) => {
    const listItem = document.createElement("li");
    listItem.innerHTML = `
      <strong>${task.title}</strong><br>
      Description: ${task.description} <br>
      Due Date: ${task.due_date || "None"} - Priority: ${task.priority || "None"} <br>
      Assigned to User: ${task.user_id || "None"}, Category: ${task.category_id || "None"} <br>
      <div class="task-actions">
        <button onclick="markComplete(${task.id}, ${task.is_complete})">${task.is_complete ? "Unmark" : "Mark"} Complete</button>
        <button onclick="deleteTask(${task.id})">Delete</button>
      </div>
    `;
    taskList.appendChild(listItem);
  });
});