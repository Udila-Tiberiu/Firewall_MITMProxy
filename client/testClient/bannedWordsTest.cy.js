describe("Banned Words Management", () => {
    const wordToAdd = "testword123";

    beforeEach(() => {
        cy.visit("http://localhost:3000");
    });

    it("adds a banned word", () => {
        cy.get('input[placeholder="Enter word..."]').type(wordToAdd);
        cy.contains("Add Word").click();
        cy.contains("td", wordToAdd).should("exist");
    });

    it("deletes a banned word", () => {
        cy.get('input[placeholder="Enter word..."]').type(wordToAdd);
        cy.contains("Remove Word").click();
        cy.contains("td", wordToAdd).should("not.exist");
    });

    it("does not add empty word", () => {
        cy.get('input').clear();
        cy.contains("Add Word").click();
    });

    it("handles fetch error gracefully", () => {
        cy.intercept("GET", "/logs/banned_words", { forceNetworkError: true }).as("getWordsFail");
        cy.reload();
        cy.wait("@getWordsFail");
        cy.contains("Banned Words");
    });
});
