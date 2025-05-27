import React, { useEffect, useState } from "react";

function LogViewer({ type }) {
    const [data, setData] = useState([]);

    useEffect(() => {
        if (!type) return;
        fetch(`http://localhost:8000/logs/${type}`)
            .then((res) => res.json())
            .then(setData)
            .catch((err) => console.error("Error fetching log:", err));
    }, [type]);

    const handleClear = () => {
        fetch(`http://localhost:8000/logs/clear/${type}`, {
            method: "POST",
        })
            .then((res) => {
                if (res.ok) setData([]);
            })
            .catch((err) => console.error("Error clearing log:", err));
    };

    return (
        <div>
            <h3>{type === "ads" ? "Blocked Ads" : "Blocked Websites (by content)"}</h3>
            <button onClick={handleClear} style={{marginBottom: "10px"}}>
                Clear Table
            </button>
            <table border="1" cellPadding="5" width="100%">
                <thead>
                <tr>
                    {type === "ads" ? (
                        <th>URL</th>
                    ) : (
                        <>
                            <th>Blocked Word</th>
                            <th>URL</th>
                        </>
                    )}
                </tr>
                </thead>
                <tbody>
                {data.map((entry, idx) => (
                    <tr key={idx}>
                        {type === "ads" ? (
                            <td>{entry}</td>
                        ) : (
                            <>
                                <td>{entry.word}</td>
                                <td>{entry.url}</td>
                            </>
                        )}
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
}

    export default LogViewer;
