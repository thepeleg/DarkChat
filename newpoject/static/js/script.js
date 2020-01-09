const socket = new WebSocket(getUrl());
// --------------------------------------------------
// החלק הזה מפעיל את כל הפעולות הכתובות בקובץ
// הפעולה מקשיבה תמיד לדרישותיו של הלקוח
// לדוגמה: אם הבקשה היא לפתוח צ'אט אז הצ'אט יוצג עם כל ההודעות השמורות שלו
ScrollToBottom();
socket.onmessage = msg =>{
  const receive = JSON.parse(msg.data);
  switch(receive['type']){
    case 'open_chat':
      DisplayChat(receive);
      break;
    case 'send_message':
      DisplayMessageByData(receive);
      break;
  }
  ScrollToBottom();
}
// --------------------------------------------------
function DisplayRightMessage(data){
  // הפעולה מקבלת את תוכן ההודעה מהלקוח ומציגה אותו בצד ימין כפי שהוגדר
  const chat = document.querySelector(".chat-body1");
  const element = document.createElement("div")
  const text = document.createElement("p");
  const time = document.createElement("span");

  element.classList.add("right-message-body");
  time.classList.add("time-right");
  text.classList.add("message-text");

  text.innerHTML = data.message;
  time.innerHTML = data.time;

  element.appendChild(text);
  element.appendChild(time);
  chat.appendChild(element);
}
function DisplayLeftMessage(data){
  // הפעולה מקבלת את תוכן ההודעה מהשרת ומציגה אותו בצד שמאל כפי שהוגדר
  const chat = document.querySelector(".chat-body1");
  const element = document.createElement("div")
  const text = document.createElement("p");
  const time = document.createElement("span");

  element.classList.add("left-message-body");
  time.classList.add("time-left");
  text.classList.add("message-text");

  text.innerHTML = data.message;
  time.innerHTML = data.time;

  element.appendChild(text);
  element.appendChild(time);
  chat.appendChild(element);
}
function getUrl() {
  // הפעולה מחזירה את כתובת הURL הסופית
   const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
   const url = `${wsScheme}://${location.hostname}:${location.port}/ws${
     location.pathname}`;
   return url.slice(0,-1);
}
function SendMessage(username){
  // פעולה המקבלת את המשתמש המתאים ושולחת את ההודעה בצירוף תכונות נוספות
  const input = document.querySelector("#message-input");
  const msg = {
    type:"new_message",
    message: input.value,
    time: getTime(),
    src: username,
    dst:getSelectedChatId()
  }
  socket.send(JSON.stringify(msg));
  input.value = '';
  return false;
}
function getTime() {
  // פעולה הלוקחת את השעה המדויקת בה נשלחה ההודעה
  var d = new Date();
  return `${addZero(d.getHours())}:${addZero(d.getMinutes())}`;
}
function addZero(num) {
  // פעולה המציגה את השעה בצורה נכונה ומתאימה יותר
 if (num < 10) {
   num = `0${num}`;
 }
 return num;
}
function ScrollToBottom() {
  // פונקציה שמוסיפה את האפשרות לגלול למטה ולמעלה את הצ'אט
  const slider = document.querySelector(".chat_area");
  slider.scrollTop = slider.scrollHeight;
}
function clearChat(){
  // פעולה המנקה את תוכן הצ'אט
  $('.chat-body1').empty();
}
function getUsername(){
  // פעולה המחזירה את שם המשתמש
  const username = document.querySelector("#hidden");
  return username.innerHTML;
}
function DisplayMessageByData(receive){
  //  הפעולה בודקת באיזה צד ההודעה צריכה להיות ולמי היא שייכת
  if(isSameChat(receive.dst))
  {
  if(receive.src == getUsername()){
    DisplayRightMessage(receive);
  }
  else{
    DisplayLeftMessage(receive);
    }
  }
}
function DisplayChat(receive){
  // הפעולה מציגה את הצ'אט
  clearChat();
  const messages = receive.messages;
  // console.log(messages);
  for(var i = 0;i<messages.length;i++){
    DisplayMessageByData(messages[i]);
  }
}
function getSelectedChatId(){
  // הפעולה מציגה את הצ'אט שנבחר על פי כתובת הצ'אט
  return document.querySelector(".chat-body1").id;
}
function RequestChat(id,friend_id,friends_name){
  // פעולה שמבקשת גישה לצ'אט על פי כתובת הID של המשתמש 
  const title = document.querySelector("#chatTitle");
  const chat = document.querySelector(".chat-body1");
  title.innerHTML = friends_name;
  const chatId = id + "Q" +friend_id
  chat.id = chatId;
  msg = {
    type:'get_chat',
    chat_id: chatId
  }
  socket.send(JSON.stringify(msg));
}
function isSameChat(messageId){
  // הפעולה בודקת האם הצ'אט של הלקוח הוא אותו צ'אט כמו של הלקוח השני
  let chatId = getSelectedChatId();
  var isSame = false;
  if(chatId == messageId){
    isSame = true;
  }
  const lst = chatId.split("Q");
  chatId = lst[1] + "Q"+ lst[0];
  if(chatId == messageId){
    isSame = true;
  }
  return isSame;
}
// פעולה שמקשיבה כל הזמן ומחפשת את שם המשתמש ברשימת הצעה לחברים ומסננת בהתאם
$(document).ready(function(){
  $("#user_input").keyup(function(){
    let filter = $(this).val();
    $("ul#chats_search a").each(function(){
      let name = $(this).find(".primary-font");
      if (name.text().search(new RegExp(filter, "i")) < 0) {
        $(this).fadeOut();
      }
      else{
        $(this).fadeIn();
      }
    })
  })
})
// פעולה שמקשיבה כל הזמן ומחפשת את שם המשתמש ברשימת חיפוש החברים ומסננת בהתאם
$(document).ready(function(){
  $("#friend_input").keyup(function(){
    let filter = $(this).val();
    $("ul#friend_search li").each(function(){
      let name = $(this).find(".primary-font");
      if (name.text().search(new RegExp(filter, "i")) < 0) {
        $(this).fadeOut();
      }
      else{
        $(this).fadeIn();
      }
    })
  })
})