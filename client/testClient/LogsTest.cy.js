describe("LogViewer", () => {
    beforeEach(() => {
        cy.visit("/");
    });

    it("loads blocked ads", () => {
        cy.contains("View Blocked Ads").click();
        cy.contains("Blocked Ads");
    });

    it("loads blocked content", () => {
        cy.contains("View Blocked Content").click();
        cy.contains("Blocked Websites (by content)");
    });

    it("clears the table", () => {
        cy.contains("View Blocked Ads").click();
        cy.intercept("POST", "/logs/clear/ads", {}).as("clearAds");
        cy.contains("Clear Table").click();
        cy.wait("@clearAds");
    });
});
