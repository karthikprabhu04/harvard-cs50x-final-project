let mediaRecorder;
let audioChunks = [];

const recordBtn = document.getElementById("recordBtn");
const stopBtn = document.getElementById("stopBtn");

recordBtn.onclick = async () => {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream);
  mediaRecorder.start();
  recordBtn.disabled = true;
  stopBtn.disabled = false;
  audioChunks = [];

  mediaRecorder.ondataavailable = e => {
    audioChunks.push(e.data);
  };

  mediaRecorder.onstop = async () => {
    const blob = new Blob(audioChunks, { type: "audio/wav" });
    const formData = new FormData();
    formData.append("audio", blob, "lecture.wav");

    const response = await fetch("/process", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    document.getElementById("transcript").textContent = data.transcript;
    document.getElementById("summary").textContent = data.summary;
    recordBtn.disabled = false;
  };
};

stopBtn.onclick = () => {
  mediaRecorder.stop();
  stopBtn.disabled = true;
};