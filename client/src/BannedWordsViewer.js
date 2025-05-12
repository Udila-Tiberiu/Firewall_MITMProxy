import React, { useEffect, useState } from "react";

function BannedWordsTable() {
    const [words, setWords] = useState([]);
    const [input, setInput] = useState("");

    const fetchWords = () => {
        fetch("http://localhost:8000/logs/banned_words")
            .then((res) => res.json())
            .then(setWords)
            .catch((err) => console.error("Error fetching banned words:", err));
    };

    useEffect(() => {
        fetchWords();
    }, []);

    const handleAdd = () => {
        if (!input.trim()) return;
        fetch("http://localhost:8000/logs/banned_words", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ word: input }),
        }).then(() => {
            setInput("");
            fetchWords();
        });
    };

    const handleDelete = () => {
        if (!input.trim()) return;
        fetch("http://localhost:8000/logs/banned_words", {
            method: "DELETE",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ word: input }),
        }).then(() => {
            setInput("");
            fetchWords();
        });
    };

    return (
        <div style={{ padding: "20px" }}>
            <nav style={{
                backgroundColor: "#333",
                color: "#fff",
                padding: "10px",
                fontSize: "18px"
            }}>
                Banned Words Management
            </nav>

            <div style={{ marginTop: "20px", marginBottom: "20px" }}>
                <input
                    type="text"
                    value={input}
                    placeholder="Enter word..."
                    onChange={(e) => setInput(e.target.value)}
                    style={{ padding: "5px", marginRight: "10px", width: "200px" }}
                />
                <button onClick={handleAdd} style={{ marginRight: "10px" }}>Add Word</button>
                <button onClick={handleDelete}>Remove Word</button>
            </div>

            <h2>Banned Words</h2>
            <div style={{ maxHeight: "300px", overflowY: "auto", border: "1px solid #ccc" }}>
                <table border="1" cellPadding="5" style={{ width: "100%", borderCollapse: "collapse" }}>
                    <thead style={{ position: "sticky", top: 0, backgroundColor: "#f0f0f0" }}>
                    <tr>
                        <th>Word</th>
                    </tr>
                    </thead>
                    <tbody>
                    {words.map((word, idx) => (
                        <tr key={idx}>
                            <td>{word}</td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

export default BannedWordsTable;
