const typingText = document.getElementById("typingText");

const firstText = {
    text: "Assalamu Alaikum ❤️",
    color: "rgb(4, 255, 4)"
};

const texts = [
    {
        text: "Welcome to NAFI Shop",
        color: "rgb(255, 0, 234)"
    },
    {
        text: "Premium Fashion",
        color: "#00ffbf"
    },
    {
        text: "New Collection Available",
        color: "#FFD700"
    }
];

function typeSentence(sentence, speed = 70) {

    return new Promise(resolve => {

        typingText.textContent = "";

        let i = 0;

        function type() {

            if (i < sentence.length) {

                typingText.textContent += sentence.charAt(i);
                i++;

                setTimeout(type, speed);

            } else {

                resolve();

            }

        }

        type();

    });

}

function erase(speed = 40) {

    return new Promise(resolve => {

        function remove() {

            if (typingText.textContent.length > 0) {

                typingText.textContent =
                    typingText.textContent.slice(0, -1);

                setTimeout(remove, speed);

            } else {

                resolve();

            }

        }

        remove();

    });

}

async function startTyping() {

    // First Message
    typingText.style.color = firstText.color;

    await typeSentence(firstText.text);

    await new Promise(r => setTimeout(r, 2000));

    typingText.classList.add("fade");

    await new Promise(r => setTimeout(r, 800));

    typingText.classList.remove("fade");

    typingText.textContent = "";

    // Loop Forever
    while (true) {

        for (let item of texts) {

            typingText.style.color = item.color;

            await typeSentence(item.text);

            await new Promise(r => setTimeout(r, 1500));

            await erase();

            await new Promise(r => setTimeout(r, 300));

        }

    }

}

startTyping();

