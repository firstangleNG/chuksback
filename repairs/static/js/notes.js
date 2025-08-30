const noteForm = document.getElementById("noteForm");
const noteInput = document.getElementById("noteInput");
const notesContainer = document.getElementById("notes-container");
const ticket_Id = localStorage.getItem("current_ticket");

const btnNote = document.getElementById("btnNote").addEventListener("click",async ()=>{

    const response = await fetch(`/repairs/note/${ticket_Id}/`,{
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    });
   openModal('spinner')
    if(!response.ok) throw new Error("Error occured while fetching note");
    const note = await response.json();
    noteInput.value = note.note || "No note available";
    closeModal()
    openModal('note')
})


// Handle note submission
noteForm.addEventListener("submit", async function(event) {
    event.preventDefault();
      const response = await fetch(`/repairs/note/create/${ticket_Id}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        body: JSON.stringify({ note: noteInput.value }),
    });

    if (response.ok) {
        noteInput.value = "";
        alert("Noted save successfully")
    } else {
        alert("Failed to add note");
    }
});

// Initialize
