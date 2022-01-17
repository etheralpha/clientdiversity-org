window.onload = showNotification();

// Loads/shows notification bar if users hasn't closed it yet
function showNotification() {
  const close = document.getElementById("notificationClose");
  const notificationId = close.getAttribute("data-notification-id");
  const notificationName = "notification-" + notificationId;
  const hide = localStorage.getItem(notificationName);
  if (hide != "true") {
    const notification = document.getElementById("notification");
    notification.style.display = "block";
  }
}
// Hides notification bar when user closes it
function hideNotification() {
  const notification = document.getElementById("notification");
  notification.style.display = "none";
  const close = document.getElementById("notificationClose");
  const notificationId = close.getAttribute("data-notification-id");
  const notificationName = "notification-" + notificationId;
  localStorage.setItem(notificationName, "true");
}