console.log("✅ Dark Pattern Scanner loaded");

// Store already-scanned texts
const scannedTexts = new Set();

let checkedCount = 0;

// ----------------------------
// Send text to backend
// ----------------------------
async function checkDarkPattern(text) {
    try {
        const response = await fetch("http://localhost:8000/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text })
        });

        if (!response.ok) {
            throw new Error(`HTTP Error ${response.status}`);
        }

        return await response.json();

    } catch (error) {
        console.error("❌ Fetch Error:", error);
        return null;
    }
}

// ----------------------------
// Filter useless elements
// ----------------------------
function isRelevantElement(el, text) {

    // Hidden elements
    if (!el.offsetParent) return false;

    // Too short
    if (text.length < 15) return false;

    // Too long
    if (text.length > 150) return false;

    // Huge containers
    if (el.children.length > 3) return false;

    // Ignore prices
    if (/₹|\$|€|£/.test(text)) return false;

    // Ignore keyboard shortcut text
    const lower = text.toLowerCase();

    if (
        lower.includes("shift") ||
        lower.includes("ctrl") ||
        lower.includes("alt")
    ) {
        return false;
    }

    // Ignore common navigation items
    const ignoreWords = [
        "home",
        "cart",
        "wishlist",
        "account",
        "orders",
        "customer service",
        "returns",
        "sell",
        "help"
    ];

    if (ignoreWords.includes(lower.trim()))
        return false;

    return true;
}

// ----------------------------
// Highlight dark pattern
// ----------------------------
function highlightElement(el, confidence) {

    el.style.outline = "3px solid red";
    el.style.backgroundColor = "rgba(255,0,0,0.15)";

    el.title =
        `Dark Pattern Detected (${Math.round(confidence * 100)}%)`;
}

// ----------------------------
// Scan page
// ----------------------------
async function scanPage() {

    const elements = document.querySelectorAll(
        "button, a, span, p"
    );

    console.log(`Found ${elements.length} elements`);

    for (const el of elements) {

        const text = el.innerText?.trim();

        if (!text) continue;

        if (!isRelevantElement(el, text))
            continue;

        // Avoid duplicate requests
        if (scannedTexts.has(text))
            continue;

        scannedTexts.add(text);

        checkedCount++;

        console.log(`Checking #${checkedCount}:`, text);

        const result = await checkDarkPattern(text);

        if (!result) continue;

        console.log("Result:", result);

        if (
            result.label === "DARK_PATTERN" &&
            result.confidence >= 0.90
        ) {

            console.log(
                `🚨 Dark Pattern Detected (${Math.round(result.confidence * 100)}%)`,
                text
            );

            highlightElement(el, result.confidence);
        }
    }

    console.log(`Scan complete. Checked ${checkedCount} elements.`);
}

// ----------------------------
// Start scan
// ----------------------------
window.addEventListener("load", () => {

    console.log("🚀 Starting scan in 2 seconds...");

    setTimeout(() => {
        scanPage();
    }, 2000);
});