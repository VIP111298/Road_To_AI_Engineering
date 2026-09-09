const input = document.querySelector(".chat-input input");
const sendButton = document.querySelector(".send-button");
const resetButton = document.querySelector(".reset-button");
const chatMessages = document.querySelector(".chat-messages");

const questionButtons = document.querySelectorAll(
    ".suggested-questions button"
);

let isBotTyping = false;

const welcomeMessage = `
    Hi! I am Vipul's AI portfolio assistant.
    Ask me about his projects, skills,
    experience or role suitability.
`;


function getBotAnswer(question) {

    const userQuestion = question.toLowerCase();

    if (
        userQuestion.includes("face") ||
        userQuestion.includes("attendance") ||
        userQuestion.includes("ai project")
    ) {
        return `
            Vipul developed a real-time Face Recognition
            Attendance System using Python, OpenCV, PyTorch,
            RetinaFace and MiniFASNet. It achieved over 95%
            authentication accuracy across 50+ registered
            users and automatically records attendance in CSV.
        `;
    }

    if (
        userQuestion.includes("skill") ||
        userQuestion.includes("technology") ||
        userQuestion.includes("tech stack")
    ) {
        return `
            Vipul works with Python, C++, JavaScript, HTML,
            CSS and SQL. His libraries and frameworks include
            PyTorch, OpenCV, Flask, NumPy, Pandas, Tkinter
            and React.
        `;
    }

    if (
        userQuestion.includes("project") ||
        userQuestion.includes("work")
    ) {
        return `
            Vipul has developed three major projects:
            a Face Recognition Attendance System,
            a Car Dealership website with a News API,
            and a Weather Forecast application using
            the OpenWeatherMap API.
        `;
    }

    if (
        userQuestion.includes("education") ||
        userQuestion.includes("college") ||
        userQuestion.includes("degree") ||
        userQuestion.includes("study")
    ) {
        return `
            Vipul is pursuing a B.Tech in Computer Science
            and Engineering with an AI and ML specialization
            from KIET Group of Institutions. He is expected
            to graduate in May 2027.
        `;
    }

    if (
        userQuestion.includes("experience") ||
        userQuestion.includes("leadership") ||
        userQuestion.includes("mlsa")
    ) {
        return `
            Vipul is the Vice President of MLSA KIET,
            where he leads a 40-member developer community.
            He has helped deliver more than 12 technical
            workshops and coordinated developer events.
        `;
    }

    if (
        userQuestion.includes("hire") ||
        userQuestion.includes("candidate") ||
        userQuestion.includes("suitable") ||
        userQuestion.includes("why vipul")
    ) {
        return `
            Vipul combines practical AI and ML development,
            web-development fundamentals and proven leadership.
            He is suitable for AI/ML internships and
            entry-level software engineering opportunities.
        `;
    }

    if (
        userQuestion.includes("contact") ||
        userQuestion.includes("email") ||
        userQuestion.includes("reach")
    ) {
        return `
            You can contact Vipul at vipxtiwari@gmail.com.
            His LinkedIn and GitHub profiles are also linked
            at the bottom of this portfolio.
        `;
    }

    if (
        userQuestion.includes("certificate") ||
        userQuestion.includes("certification")
    ) {
        return `
            Vipul has certifications from AWS,
            MongoDB University and Palo Alto Networks
            Cybersecurity Academy.
        `;
    }

    return `
        I do not have verified information about that yet.
        You can ask about Vipul's skills, projects,
        education, leadership or role suitability.
    `;
}


function addUserMessage(message) {

    const messageElement = document.createElement("div");

    messageElement.classList.add("user-message");
    messageElement.textContent = message;

    chatMessages.appendChild(messageElement);

    scrollToLatestMessage();
}


function addBotMessage(message) {

    const messageElement = document.createElement("div");

    messageElement.classList.add("bot-message");
    messageElement.textContent = message.trim();

    chatMessages.appendChild(messageElement);

    scrollToLatestMessage();
}


function showTypingIndicator() {

    const typingElement = document.createElement("div");

    typingElement.classList.add("typing-indicator");
    typingElement.id = "typing-indicator";

    typingElement.innerHTML = `
        <span></span>
        <span></span>
        <span></span>
    `;

    chatMessages.appendChild(typingElement);

    scrollToLatestMessage();
}


function removeTypingIndicator() {

    const typingElement = document.getElementById(
        "typing-indicator"
    );

    if (typingElement) {
        typingElement.remove();
    }
}


function scrollToLatestMessage() {

    chatMessages.scrollTop = chatMessages.scrollHeight;
}


function setChatDisabled(disabled) {

    sendButton.disabled = disabled;
    input.disabled = disabled;

    questionButtons.forEach(function (button) {
        button.disabled = disabled;
    });
}


async function sendMessage(question) {

    const cleanedQuestion = question.trim();

    if (cleanedQuestion === "" || isBotTyping) {
        return;
    }

    addUserMessage(cleanedQuestion);

    input.value = "";

    isBotTyping = true;

    setChatDisabled(true);
    showTypingIndicator();

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/chat",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    question: cleanedQuestion
                })
            }
        );

        if (!response.ok) {
            throw new Error(
                "Backend response failed"
            );
        }

        const data = await response.json();

        addBotMessage(data.answer);

    } catch (error) {

        console.error(
            "Chat error:",
            error
        );

        addBotMessage(
            "Sorry, I could not connect to the AI assistant. " +
            "Please make sure the backend server is running."
        );

    } finally {

        removeTypingIndicator();

        isBotTyping = false;

        setChatDisabled(false);

        input.focus();
    }
}


sendButton.addEventListener("click", function () {
    sendMessage(input.value);
});


input.addEventListener("keydown", function (event) {

    if (event.key === "Enter") {
        sendMessage(input.value);
    }

});


questionButtons.forEach(function (button) {

    button.addEventListener("click", function () {
        sendMessage(button.textContent);
    });

});


resetButton.addEventListener("click", function () {

    isBotTyping = false;

    chatMessages.innerHTML = "";

    addBotMessage(welcomeMessage);

    setChatDisabled(false);

    input.value = "";
    input.focus();

});

const revealSections = document.querySelectorAll(
    ".technology-section, .about-section, footer"
);

revealSections.forEach(function (section) {
    section.classList.add("reveal");
});


const revealObserver = new IntersectionObserver(
    function (entries) {

        entries.forEach(function (entry) {

            if (entry.isIntersecting) {
                entry.target.classList.add("visible");

                revealObserver.unobserve(entry.target);
            }

        });

    },
    {
        threshold: 0.15
    }
);


revealSections.forEach(function (section) {
    revealObserver.observe(section);
});