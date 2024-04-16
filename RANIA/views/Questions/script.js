import { GoogleGenerativeAI } from "https://esm.run/@google/generative-ai"

    document.addEventListener('DOMContentLoaded', () => {
            const genAI = new GoogleGenerativeAI('AIzaSyCZO-WcADjp8Gzxtii4kSl1fGhVX3R7K50');
            const model = genAI.getGenerativeModel({ model: "gemini-pro" });
            const chat = model.startChat();

            const button = document.getElementById('submit-button');
            button.onclick = function(){
                showLoadingIndicator();
                const inputData = document.getElementById('newMessages').value;
                processData(inputData); 
                document.getElementById('newMessages').value = '';
            }

            document.addEventListener("keydown", function (event) {
                if (event.keyCode == 13) {
                    showLoadingIndicator();
                    const inputData = document.getElementById('newMessages').value;
                    processData(inputData); 
                    document.getElementById('newMessages').value = '';
                }
             });

            function showLoadingIndicator() {
                document.getElementById("submit-button").textContent = "Loading...";
              }
              
              function hideLoadingIndicator() {
                document.getElementById("submit-button").textContent = "Send";
              }

        async function processData(inputData) {
            try {
                const prompt = inputData;
            
                const result = await chat.sendMessage(prompt);
                const response = await result.response;
                const text = await response.text();

                var messagesDiv = document.getElementById("messages");
                var newMessageDivPrompt = document.createElement("div");
                newMessageDivPrompt.style.marginBottom = "10px";
                newMessageDivPrompt.style.backgroundColor = "#999999";
                newMessageDivPrompt.style.color = "#000000";
                var newMessageDivResponse = document.createElement("div");
                newMessageDivResponse.style.marginBottom = "30px";
                newMessageDivResponse.style.backgroundColor = "#f0f0f0";
                newMessageDivResponse.style.color = "#000000";
                newMessageDivPrompt.textContent = prompt;
                messagesDiv.appendChild(newMessageDivPrompt);
                newMessageDivResponse.textContent = text;
                messagesDiv.appendChild(newMessageDivResponse);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
                hideLoadingIndicator();
            } catch (error) {
                console.error('An error occurred:', error);
                return null;
            }
        }

    });