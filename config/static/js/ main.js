window.addEventListener("scroll",function(){

    const navbar=document.querySelector(".custom-navbar");

    navbar.classList.toggle("scrolled",window.scrollY>40);

});

// Sticky Navbar

window.addEventListener("scroll", () => {

    const navbar = document.querySelector(".custom-navbar");

    navbar.classList.toggle("scrolled", window.scrollY > 40);

});

// Scroll Progress

window.addEventListener("scroll", () => {

    let scrollTop = document.documentElement.scrollTop;

    let scrollHeight =
        document.documentElement.scrollHeight -
        document.documentElement.clientHeight;

    let progress = (scrollTop / scrollHeight) * 100;

    document.querySelector(".scroll-progress").style.width =
        progress + "%";

});

// Active Navbar

const sections = document.querySelectorAll("section");

const navLinks = document.querySelectorAll(".nav-link");

window.addEventListener("scroll", () => {

    let current = "";

    sections.forEach(section => {

        const sectionTop = section.offsetTop - 120;

        if (pageYOffset >= sectionTop) {

            current = section.getAttribute("id");

        }

    });
//Premium Nav BAR LINk
    navLinks.forEach(link => {

        link.classList.remove("active");

        if (link.getAttribute("href") == "#" + current) {

            link.classList.add("active");

        }

    });

});
//Hero Fade-in Animation
window.addEventListener("load",()=>{

document.querySelector(".hero-title").classList.add("show");

document.querySelector(".hero-text").classList.add("show");

});

///*==================================
//      Counter Animation in statistics
//===================================*/
//
//document.addEventListener("DOMContentLoaded", function () {
//
//    const counters = document.querySelectorAll(".counter");
//
//    counters.forEach(counter => {
//
//        const target = +counter.dataset.target;
//
//        const updateCounter = () => {
//
//            const count = +counter.innerText.replace("+","");
//
//            const increment = target / 150;
//
//            if(count < target){
//
//                counter.innerText = Math.ceil(count + increment);
//
//                setTimeout(updateCounter,15);
//
//            }else{
//
//                counter.innerText = target.toLocaleString() + "+";
//
//            }
//
//        };
//
//        updateCounter();
//
//    });
//
//});
/*==================================
      Counter Animation
===================================*/

const counters = document.querySelectorAll('.counter');

counters.forEach(counter=>{

    const updateCounter=()=>{

        const target = +counter.getAttribute('data-target');

        const count = +counter.innerText;

        const increment = target/150;

        if(count<target){

            counter.innerText=Math.ceil(count+increment);

            setTimeout(updateCounter,15);

        }

        else{

            counter.innerText=target.toLocaleString()+"+";

        }

    }

    updateCounter();

});