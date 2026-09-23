async function generateResponse(task) {

    const content =
        document.getElementById("content").value.trim();

    const message =
        document.getElementById("message");

    const result =
        document.getElementById("result");


    // Validate empty input

    if (!content) {

        message.textContent =
            "⚠️ Please enter some content first.";

        message.style.color = "red";

        return;
    }


    // Validate very short input

    if (content.length < 10) {

        message.textContent =
            "⚠️ Please enter a little more information.";

        message.style.color = "red";

        return;
    }


    // Show loading message

    message.textContent =
        "🤖 AI is thinking...";

    message.style.color = "#4f46e5";


    result.textContent =
        "Generating your response...";


    try {

        const response =
            await fetch("/generate", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    task: task,

                    content: content

                })

            });


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error ||
                "Something went wrong."
            );

        }


        // Display AI response

        result.textContent =
            data.result;


        message.textContent =
            "✅ Response generated successfully!";

        message.style.color = "green";


    } catch (error) {

        console.error(error);


        result.textContent =
            "No response was generated.";


        message.textContent =
            "❌ " + error.message;

        message.style.color = "red";

    }

}