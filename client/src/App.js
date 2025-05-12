import React, { useState } from "react";
import LogViewer from "./LogViewer";
import BannedWordsTable from "./BannedWordsViewer";
import Modal from "react-modal";

// Bind modal to root app element
Modal.setAppElement("#root");

function App() {
    const [modalType, setModalType] = useState(null);

    const closeModal = () => setModalType(null);

    return (
        <div className="App">
            {/* Navbar */}
            <nav style={{
                backgroundColor: "#282c34",
                padding: "10px 20px",
                color: "white",
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center"
            }}>
                <h2>Ad & Content Blocker</h2>
                <div>
                    <button onClick={() => setModalType("ads")} style={{ marginRight: "10px" }}>
                        View Blocked Ads
                    </button>
                    <button onClick={() => setModalType("content")}>
                        View Blocked Content
                    </button>
                </div>
            </nav>
            <BannedWordsTable />
            {/* Modal */}
            <Modal
                isOpen={!!modalType}
                onRequestClose={closeModal}
                contentLabel="Log Viewer"
                style={{
                    content: {
                        top: '50%',
                        left: '50%',
                        right: 'auto',
                        bottom: 'auto',
                        marginRight: '-50%',
                        transform: 'translate(-50%, -50%)',
                        maxHeight: '80vh',
                        overflowY: 'auto',
                        width: '600px',
                        padding: '20px'
                    }
                }}
            >

                <button onClick={closeModal} style={{ float: "right" }}>Close</button>
                <LogViewer type={modalType} />
            </Modal>
        </div>
    );
}

export default App;
