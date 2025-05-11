import React, { useEffect, useState } from "react";

function LogViewer() {
    const [ads, setAds] = useState([]);
    const [content, setContent] = useState([]);

    useEffect(() => {
        fetch("http://localhost:5000/logs/ads")
            .then((res) => res.json())
            .then(setAds)
            .catch((err) => console.error("Error fetching ads log:", err));

        fetch("http://localhost:5000/logs/content")
            .then((res) => res.json())
            .then(setContent)
            .catch((err) => console.error("Error fetching content log:", err));
    }, []);

    return (
        <div style={{ padding: "20px" }}>
            <h2>Blocked Ads</h2>
            <table border="1" cellPadding="5">
                <thead>
                <tr>
                    <th>URL</th>
                </tr>
                </thead>
                <tbody>
                {ads.map((url, idx) => (
                    <tr key={idx}>
                        <td>{url}</td>
                    </tr>
                ))}
                </tbody>
            </table>

            <h2 style={{ marginTop: "40px" }}>Blocked Websites (by content)</h2>
            <table border="1" cellPadding="5">
                <thead>
                <tr>
                    <th>URL</th>
                </tr>
                </thead>
                <tbody>
                {content.map((url, idx) => (
                    <tr key={idx}>
                        <td>{url}</td>
                    </tr>
                ))}
                </tbody>
            </table>
        </div>
    );
}

export default LogViewer;
