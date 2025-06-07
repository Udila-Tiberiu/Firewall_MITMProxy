describe("App Component", () => {
    beforeEach(() => {
        cy.visit("/");
    });

    it("opens and closes the ads modal", () => {
        cy.contains("View Blocked Ads").click();
        cy.contains("Blocked Ads").should("exist");
        cy.contains("Close").click();
    });

    it("opens and closes the content modal", () => {
        cy.contains("View Blocked Content").click();
        cy.contains("Blocked Websites (by content)").should("exist");
        cy.contains("Close").click();
    });

    it("opens and closes the Help modal", () => {
        cy.contains("Help").click();
        cy.contains("Help Guide").should("exist");
        cy.contains("Close").click();
    });
});
