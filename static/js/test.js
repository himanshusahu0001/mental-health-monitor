const questions = [
    "Little interest or pleasure in doing things?",
    "Feeling down, depressed, or hopeless?",
    "Trouble falling or staying asleep, or sleeping too much?",
    "Feeling tired or having little energy?",
    "Poor appetite or overeating?",
    "Feeling bad about yourself — or that you are a failure or have let yourself or your family down?",
    "Trouble concentrating on things, such as reading the newspaper or watching television?",
    "Moving or speaking so slowly that other people could have noticed? Or so fidgety or restless that you have been moving a lot more than usual?",
    "Thoughts that you would be better off dead, or thoughts of hurting yourself in some way?"
]

const answers = [
    "Not at all",
    "Several days",
    "More than half the days",
    "Nearly every day"
]

const question = document.getElementById('question')
const answerButtons = document.getElementById("answer-buttons"); 
const nextBtn = document.querySelector(".next-btn"); 
let currentIndex = 0;
let score=0;

function startQuiz(){
    showQuestion();
};

function showQuestion() {
    question.innerHTML = questions[currentIndex];

    answerButtons.innerHTML = "";
    answers.forEach((answer,index)=>{
        const answerButton = document.createElement("label");
        answerButton.classList.add(`btn`, "radio-button", `btn_${index}`);

        answerButton.innerHTML = `
        <input type="radio" name="question" value="${index}" class="radio-button">
        <span>${answer}</span>
        `;
        answerButtons.appendChild(answerButton);
    });

    const radioButtons = document.querySelectorAll('.radio-button input[type="radio"]');

    radioButtons.forEach(radioButton => {
      radioButton.addEventListener('change', () => {
        const parentLabels = document.querySelectorAll('.radio-button');
        
        parentLabels.forEach(label => {
          label.classList.remove('checked');
        });
    
        const parentLabel = radioButton.parentNode;
        parentLabel.classList.add('checked');
      });
    });
    
};



function handleNextButtonClick() {
  const selectedAnswer = document.querySelector('input[name="question"]:checked');
  
  if (!selectedAnswer) {
    // If no answer is selected, show an alert or error message
    alert("Please select an answer.");
    return;
  }
  
  // Do something with the selected answer, e.g., store it or perform calculations
  score += parseInt(selectedAnswer.value);
  
  currentIndex++; // Move to the next question
  
  if (currentIndex < questions.length) {
      // If there are more questions, show the next question
    showQuestion(currentIndex);
  } else {
    // If all questions are answered, do something (e.g., show results)
    // alert("Quiz completed!");
    
    
    console.log(score);
    /* in question ele. add quiz completed, and make a submit button to send ans to server */
    question.innerHTML = "Questionaire Completed!";
    answerButtons.innerHTML = "";
    
    nextBtn.style.display = 'none';

    const submit = document.getElementById('submit');
    submit.style.display = 'block'; 
    
    inputScore = document.getElementById('scoreInput');
    inputScore.value = score;

  }
}
nextBtn.addEventListener("click", handleNextButtonClick);


startQuiz();

