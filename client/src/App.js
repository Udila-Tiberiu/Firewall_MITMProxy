import React, { useState } from "react";
import LogViewer from "./LogViewer";
import BannedWordsTable from "./BannedWordsViewer";
import Modal from "react-modal";
import Help1 from './Help1.png';
import Help2 from './Help2.png';
import Help3 from './Help3.png';


Modal.setAppElement("#root");

function App() {
    const [modalType, setModalType] = useState(null);
    const [helpOpen, setHelpOpen] = useState(false);

    const closeModal = () => setModalType(null);
    const openHelp = () => setHelpOpen(true);
    const closeHelp = () => setHelpOpen(false);

    return (
        <div className="App" style={{ position: "relative", minHeight: "100vh" }}>
            {/* Navbar */}
            <nav
                style={{
                    backgroundColor: "#282c34",
                    padding: "10px 20px",
                    color: "white",
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                }}
            >
                <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>

                    <h2>Ad Blocker and Unwanted Content Filter</h2>
                </div>
                <div>
                    <button onClick={() => setModalType("ads")} style={{ marginRight: "10px" }}>
                        View Blocked Ads
                    </button>
                    <button onClick={() => setModalType("content")}>View Blocked Content</button>
                </div>
            </nav>


            <BannedWordsTable />

            <Modal
                isOpen={!!modalType}
                onRequestClose={closeModal}
                contentLabel="Log Viewer"
                style={{
                    content: {
                        top: "50%",
                        left: "50%",
                        right: "auto",
                        bottom: "auto",
                        marginRight: "-50%",
                        transform: "translate(-50%, -50%)",
                        maxHeight: "80vh",
                        overflowY: "auto",
                        width: "600px",
                        padding: "20px",
                    },
                }}
            >
                <button onClick={closeModal} style={{ float: "right" }}>
                    Close
                </button>
                <LogViewer type={modalType} />
            </Modal>

            <button
                onClick={openHelp}
                style={{
                    position: "fixed",
                    bottom: "20px",
                    right: "20px",
                    padding: "10px 20px",
                    backgroundColor: "#282c34",
                    color: "white",
                    border: "none",
                    borderRadius: "8px",
                    cursor: "pointer",
                    boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
                }}
            >
                Help
            </button>

            <Modal
                isOpen={helpOpen}
                onRequestClose={closeHelp}
                contentLabel="Help Modal"
                style={{
                    content: {
                        top: "50%",
                        left: "50%",
                        right: "auto",
                        bottom: "auto",
                        marginRight: "-50%",
                        transform: "translate(-50%, -50%)",
                        width: "80vw",
                        maxHeight: "80vh",
                        overflowY: "auto",
                        padding: "20px",
                    },
                }}
            >
                <button onClick={closeHelp} style={{ float: "right" }}>
                    Close
                </button>
                <h2>Help Guide</h2>
                <div style={{ marginTop: "20px", display: "flex", flexDirection: "column", gap: "20px" }}>
                    <img src={Help1} alt="Help Step 1" style={{ width: "100%", maxHeight: "40vh", objectFit: "contain" }} />
                    <div style={{ display: "flex", gap: "20px" }}>
                        <img src={Help2} alt="Help Step 2" style={{ width: "48%", maxHeight: "25vh", objectFit: "contain" }} />
                        <img src={Help3} alt="Help Step 3" style={{ width: "48%", maxHeight: "25vh", objectFit: "contain" }} />
                    </div>
                </div>
            </Modal>
        </div>
    );
}

export default App;
