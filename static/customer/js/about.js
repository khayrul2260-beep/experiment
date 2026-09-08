document.addEventListener("DOMContentLoaded", () => {

    const page = document.querySelector(".nafi-about-page");

    if (!page) return;


    /* =========================================================
       REDUCED MOTION
    ========================================================= */

    const reduceMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    ).matches;


    /* =========================================================
       HERO
    ========================================================= */

    const hero = page.querySelector(".about-hero");
    const heroImage = page.querySelector(".about-hero-image img");
    const heroContent = page.querySelector(".about-hero-content");
    const heroScroll = page.querySelector(".about-scroll-indicator");


    if (hero && !reduceMotion) {

        hero.classList.add("hero-ready");

        requestAnimationFrame(() => {

            setTimeout(() => {
                hero.classList.add("hero-loaded");
            }, 120);

        });

    }


    /* =========================================================
       HERO PARALLAX
    ========================================================= */

    if (
        hero &&
        heroImage &&
        window.innerWidth > 768 &&
        !reduceMotion
    ) {

        let ticking = false;

        const updateHero = () => {

            const rect = hero.getBoundingClientRect();

            if (
                rect.bottom > 0 &&
                rect.top < window.innerHeight
            ) {

                const progress =
                    Math.max(
                        -1,
                        Math.min(
                            1,
                            rect.top / window.innerHeight
                        )
                    );

                const movement = progress * 25;

                heroImage.style.transform =
                    `translate3d(0, ${movement}px, 0) scale(1.035)`;
            }

            ticking = false;
        };


        window.addEventListener(
            "scroll",
            () => {

                if (!ticking) {

                    requestAnimationFrame(updateHero);

                    ticking = true;
                }

            },
            { passive: true }
        );

    }


    /* =========================================================
       HERO SCROLL INDICATOR
    ========================================================= */

    if (heroScroll && hero && !reduceMotion) {

        heroScroll.addEventListener("click", () => {

            const nextSection =
                hero.nextElementSibling;

            if (!nextSection) return;

            nextSection.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        });


        const updateScrollIndicator = () => {

            const opacity =
                Math.max(
                    0,
                    1 - window.scrollY / 180
                );

            heroScroll.style.opacity = opacity;

        };


        window.addEventListener(
            "scroll",
            updateScrollIndicator,
            { passive: true }
        );

    }


    /* =========================================================
       SECTION REVEAL
    ========================================================= */

    const sections = page.querySelectorAll(
        ".about-section"
    );


    if (reduceMotion) {

        sections.forEach(section => {
            section.classList.add("is-visible");
        });

    } else if ("IntersectionObserver" in window) {

        const sectionObserver =
            new IntersectionObserver(
                (entries, observer) => {

                    entries.forEach(entry => {

                        if (!entry.isIntersecting) return;

                        entry.target.classList.add(
                            "is-visible"
                        );

                        observer.unobserve(
                            entry.target
                        );

                    });

                },
                {
                    threshold: 0.16,
                    rootMargin: "0px 0px -80px 0px"
                }
            );


        sections.forEach(section => {

            section.classList.add(
                "section-hidden"
            );

            sectionObserver.observe(section);

        });

    }


    /* =========================================================
       TEXT REVEAL
    ========================================================= */

    const textElements = page.querySelectorAll(
        ".about-section-number, " +
        ".about-text h2, " +
        ".about-text h3, " +
        ".about-text p, " +
        ".about-section-heading h2, " +
        ".about-section-heading p, " +
        ".about-vision-content h2, " +
        ".about-vision-content h3, " +
        ".about-vision-content p, " +
        ".about-final-content strong"
    );


    if (!reduceMotion && "IntersectionObserver" in window) {

        const textObserver =
            new IntersectionObserver(
                (entries, observer) => {

                    entries.forEach(entry => {

                        if (!entry.isIntersecting) return;

                        entry.target.classList.add(
                            "text-visible"
                        );

                        observer.unobserve(
                            entry.target
                        );

                    });

                },
                {
                    threshold: 0.2,
                    rootMargin: "0px 0px -60px 0px"
                }
            );


        textElements.forEach(element => {

            element.classList.add(
                "text-hidden"
            );

            textObserver.observe(element);

        });

    } else {

        textElements.forEach(element => {

            element.classList.add(
                "text-visible"
            );

        });

    }


    /* =========================================================
       DIVIDER REVEAL
    ========================================================= */

    const dividers =
        page.querySelectorAll(
            ".about-divider"
        );


    if (!reduceMotion && "IntersectionObserver" in window) {

        const dividerObserver =
            new IntersectionObserver(
                (entries, observer) => {

                    entries.forEach(entry => {

                        if (!entry.isIntersecting) return;

                        entry.target.classList.add(
                            "divider-visible"
                        );

                        observer.unobserve(
                            entry.target
                        );

                    });

                },
                {
                    threshold: 0.5
                }
            );


        dividers.forEach(divider => {

            divider.classList.add(
                "divider-hidden"
            );

            dividerObserver.observe(divider);

        });

    } else {

        dividers.forEach(divider => {

            divider.classList.add(
                "divider-visible"
            );

        });

    }


    /* =========================================================
       VALUE CARDS
    ========================================================= */

    const valueCards =
        page.querySelectorAll(
            ".about-value-card"
        );


    if (!reduceMotion && "IntersectionObserver" in window) {

        const valueObserver =
            new IntersectionObserver(
                (entries, observer) => {

                    entries.forEach(entry => {

                        if (!entry.isIntersecting) return;

                        const cards =
                            entry.target.querySelectorAll(
                                ".about-value-card"
                            );

                        cards.forEach((card, index) => {

                            setTimeout(() => {

                                card.classList.add(
                                    "card-visible"
                                );

                            }, index * 120);

                        });

                        observer.unobserve(
                            entry.target
                        );

                    });

                },
                {
                    threshold: 0.15
                }
            );


        const valueGrid =
            page.querySelector(
                ".about-values-grid"
            );


        if (valueGrid) {

            valueCards.forEach(card => {

                card.classList.add(
                    "card-hidden"
                );

            });

            valueObserver.observe(
                valueGrid
            );

        }

    } else {

        valueCards.forEach(card => {

            card.classList.add(
                "card-visible"
            );

        });

    }


    /* =========================================================
       QUALITY CARDS
    ========================================================= */

    const qualityGrid =
        page.querySelector(
            ".about-quality-grid"
        );

    const qualityCards =
        page.querySelectorAll(
            ".about-quality-card"
        );


    if (qualityGrid) {

        if (!reduceMotion) {

            qualityCards.forEach(card => {

                card.classList.add(
                    "card-hidden"
                );

            });


            const qualityObserver =
                new IntersectionObserver(
                    (entries, observer) => {

                        entries.forEach(entry => {

                            if (!entry.isIntersecting)
                                return;

                            qualityCards.forEach(
                                (card, index) => {

                                    setTimeout(() => {

                                        card.classList.add(
                                            "card-visible"
                                        );

                                    }, index * 110);

                                }
                            );

                            observer.unobserve(
                                entry.target
                            );

                        });

                    },
                    {
                        threshold: 0.15
                    }
                );


            qualityObserver.observe(
                qualityGrid
            );

        } else {

            qualityCards.forEach(card => {

                card.classList.add(
                    "card-visible"
                );

            });

        }

    }


    /* =========================================================
       TIMELINE
    ========================================================= */

    const timeline =
        page.querySelector(
            ".about-timeline"
        );

    const timelineItems =
        page.querySelectorAll(
            ".about-timeline-item"
        );


    if (timeline && !reduceMotion) {

        timelineItems.forEach(item => {

            item.classList.add(
                "timeline-hidden"
            );

        });


        const timelineObserver =
            new IntersectionObserver(
                (entries, observer) => {

                    entries.forEach(entry => {

                        if (!entry.isIntersecting)
                            return;

                        timelineItems.forEach(
                            (item, index) => {

                                setTimeout(() => {

                                    item.classList.add(
                                        "timeline-visible"
                                    );

                                }, index * 180);

                            }
                        );

                        observer.unobserve(
                            entry.target
                        );

                    });

                },
                {
                    threshold: 0.12
                }
            );


        timelineObserver.observe(
            timeline
        );

    } else {

        timelineItems.forEach(item => {

            item.classList.add(
                "timeline-visible"
            );

        });

    }


    /* =========================================================
       PROFILE ITEMS
    ========================================================= */

    const profileItems =
        page.querySelectorAll(
            ".about-profile-item"
        );


    if (!reduceMotion) {

        profileItems.forEach((item, index) => {

            item.style.transitionDelay =
                `${index * 90}ms`;

        });

    }


    /* =========================================================
       IMAGE REVEAL
    ========================================================= */

    const images =
        page.querySelectorAll(
            ".about-image, " +
            ".about-timeline-content img, " +
            ".about-final-image"
        );


    if (!reduceMotion && "IntersectionObserver" in window) {

        const imageObserver =
            new IntersectionObserver(
                (entries, observer) => {

                    entries.forEach(entry => {

                        if (!entry.isIntersecting)
                            return;

                        entry.target.classList.add(
                            "image-visible"
                        );

                        observer.unobserve(
                            entry.target
                        );

                    });

                },
                {
                    threshold: 0.15
                }
            );


        images.forEach(image => {

            image.classList.add(
                "image-hidden"
            );

            imageObserver.observe(
                image
            );

        });

    } else {

        images.forEach(image => {

            image.classList.add(
                "image-visible"
            );

        });

    }


    /* =========================================================
       FINAL SECTION
    ========================================================= */

    const finalSection =
        page.querySelector(
            ".about-final"
        );


    if (
        finalSection &&
        !reduceMotion &&
        "IntersectionObserver" in window
    ) {

        const finalObserver =
            new IntersectionObserver(
                (entries, observer) => {

                    entries.forEach(entry => {

                        if (!entry.isIntersecting)
                            return;

                        entry.target.classList.add(
                            "final-visible"
                        );

                        observer.unobserve(
                            entry.target
                        );

                    });

                },
                {
                    threshold: 0.2
                }
            );


        finalObserver.observe(
            finalSection
        );

    } else if (finalSection) {

        finalSection.classList.add(
            "final-visible"
        );

    }

});