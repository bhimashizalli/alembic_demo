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
  
  document.getElementById("createTaskForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;
    const user_id = document.getElementById("user_id").value;
    const due_date = document.getElementById("due_date").value;
    const category_id = document.getElementById("category_id").value;
  
    const response = await fetch("/task", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, description, user_id, due_date, category_id }),
    });
  
    const data = await response.json();
    alert(data.message || data.error);
  });
  
  document.getElementById("loadTasks").addEventListener("click", async () => {
    const response = await fetch("/tasks");
    const tasks = await response.json();
  
    const taskList = document.getElementById("taskList");
    taskList.innerHTML = "";
  
    tasks.forEach((task) => {
      const listItem = document.createElement("li");
      listItem.textContent = `${task.title}: ${task.description} (Complete: ${task.is_complete}, Due: ${task.due_date}, Category: ${task.category_id})`;
      taskList.appendChild(listItem);
    });
  });