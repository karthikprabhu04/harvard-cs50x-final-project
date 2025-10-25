let mediaRecorder;
let audioChunks = [];

const recordBtn = document.getElementById("recordBtn");
const stopBtn = document.getElementById("stopBtn");
const loader = document.getElementById("loader");
const statusText = document.getElementById("status");
const transcriptEl = document.getElementById("transcript");
const summaryEl = document.getElementById("summary");

recordBtn.onclick = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.start();
    recordBtn.disabled = true;
    stopBtn.disabled = false;
    statusText.textContent = "🎙️ Recording... Speak now.";
    transcriptEl.textContent = "";
    summaryEl.textContent = "";

    mediaRecorder.ondataavailable = (e) => {
      audioChunks.push(e.data);
    };

    mediaRecorder.onstop = async () => {
      statusText.textContent = "⏳ Processing audio...";
      loader.style.display = "inline-block";

      const blob = new Blob(audioChunks, { type: "audio/wav" });
      const formData = new FormData();
      formData.append("audio", blob, "lecture.wav");

      try {
        const response = await fetch("/process", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) throw new Error("Failed to process audio.");

        const data = await response.json();

        transcriptEl.textContent = data.transcript || "No transcript available.";
        summaryEl.textContent = data.summary || "No summary available.";

        statusText.textContent = "✅ Done! Transcript and summary ready.";
      } catch (err) {
        console.error(err);
        statusText.textContent = "❌ Error processing the audio. Please try again.";
      } finally {
        loader.style.display = "none";
        recordBtn.disabled = false;
        stopBtn.disabled = true;
      }
    };
  } catch (err) {
    console.error("Microphone access denied:", err);
    alert("Please allow microphone access to record audio.");
  }
};

stopBtn.onclick = () => {
  if (mediaRecorder && mediaRecorder.state === "recording") {
    mediaRecorder.stop();
    stopBtn.disabled = true;
    statusText.textContent = "⏹️ Recording stopped. Processing...";
  }
};
