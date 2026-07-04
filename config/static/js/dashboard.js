// ===============================
// Dashboard Loaded
// ===============================

document.addEventListener("DOMContentLoaded", function () {

    // Card Hover Animation
    const cards = document.querySelectorAll(".dashboard-card");

    cards.forEach(card => {

        card.addEventListener("mouseenter", () => {

            card.style.transform = "translateY(-8px) scale(1.02)";

        });

        card.addEventListener("mouseleave", () => {

            card.style.transform = "translateY(0) scale(1)";

        });

    });

    // Counter Animation
    const numbers = document.querySelectorAll(".card-info h3");

    numbers.forEach(counter => {

        const target = counter.innerText;

        if (!isNaN(parseInt(target))) {

            let count = 0;

            const end = parseInt(target);

            const speed = Math.ceil(end / 40);

            const timer = setInterval(() => {

                count += speed;

                if (count >= end) {

                    counter.innerText = end;

                    clearInterval(timer);

                } else {

                    counter.innerText = count;

                }

            }, 30);

        }

    });

});


/*=========================================
      Study Material Search
Searches study materials in real-time
=========================================*/
const search = document.getElementById("materialSearch");

search.addEventListener("keyup",function(){

    let value = this.value.toLowerCase();

    document.querySelectorAll(".material-card").forEach(card=>{

        card.style.display =

        card.innerText.toLowerCase().includes(value)

        ? "block"

        : "none";

    });

});

const filter = document.getElementById("courseFilter");

filter.addEventListener("change",function(){

    const value = this.value;

    document.querySelectorAll(".material-card").forEach(card=>{

        if(

            value==="all" ||

            card.dataset.course===value

        ){

            card.style.display="block";

        }

        else{

            card.style.display="none";

        }

    });

});

const quizSearch=document.getElementById("quizSearch");

quizSearch.addEventListener("keyup",function(){

    let value=this.value.toLowerCase();

    document.querySelectorAll(".quiz-card").forEach(card=>{

        card.style.display=

        card.innerText.toLowerCase().includes(value)

        ?"block"

        :"none";

    });

});