document.addEventListener("DOMContentLoaded", () => {
  "use strict";

  /* =========================================================
     ELEMENTS
  ========================================================= */

  const searchInput = document.getElementById("inventorySearch");
  const stockFilter = document.getElementById("stockStatusFilter");
  const categoryFilter = document.getElementById(
    "inventoryCategoryFilter"
  );

  const refreshButton = document.getElementById(
    "inventoryRefreshBtn"
  );

  const modal = document.getElementById(
    "inventoryStockModal"
  );

  const modalOverlay = modal
    ? modal.querySelector(".inventory-modal-overlay")
    : null;

  const modalClose = document.getElementById(
    "inventoryModalClose"
  );

  const modalCancel = document.getElementById(
    "inventoryModalCancel"
  );

  const modalSave = document.getElementById(
    "inventoryModalSave"
  );

  const modalProductName = document.getElementById(
    "inventoryModalProductName"
  );

  const modalTotal = document.getElementById(
    "inventoryModalTotal"
  );

  const stockM = document.getElementById(
    "stockSizeM"
  );

  const stockL = document.getElementById(
    "stockSizeL"
  );

  const stockXL = document.getElementById(
    "stockSizeXL"
  );

  const stockXXL = document.getElementById(
    "stockSizeXXL"
  );

  const tableBody = document.getElementById(
    "inventoryTableBody"
  );

  const emptyState = document.getElementById(
    "inventoryEmptyState"
  );

  const mobileList = document.getElementById(
    "inventoryMobileList"
  );


  /* =========================================================
     STATE
  ========================================================= */

  let activeProductId = null;

  let activeProductRow = null;

  let activeMobileCard = null;


  /* =========================================================
     CSRF
  ========================================================= */

  function getCSRFToken() {

    const csrfInput = document.querySelector(
      "#inventoryCsrfForm input[name='csrfmiddlewaretoken']"
    );

    if (csrfInput) {
      return csrfInput.value;
    }

    const cookies = document.cookie.split(";");

    for (let cookie of cookies) {

      cookie = cookie.trim();

      if (cookie.startsWith("csrftoken=")) {

        return decodeURIComponent(
          cookie.substring("csrftoken=".length)
        );

      }
    }

    return "";
  }


  /* =========================================================
     STATUS
  ========================================================= */

  function getStockStatus(total) {

    total = Number(total) || 0;

    if (total === 0) {
      return "out-of-stock";
    }

    if (total <= 5) {
      return "low-stock";
    }

    return "in-stock";
  }


  function getStatusLabel(status) {

    if (status === "in-stock") {
      return "In Stock";
    }

    if (status === "low-stock") {
      return "Low Stock";
    }

    return "Out of Stock";
  }


  /* =========================================================
     MODAL TOTAL
  ========================================================= */

  function getInputValue(input) {

    if (!input) {
      return 0;
    }

    const value = parseInt(
      input.value,
      10
    );

    if (Number.isNaN(value)) {
      return 0;
    }

    return Math.max(0, value);
  }


  function calculateModalTotal() {

    const total =
      getInputValue(stockM) +
      getInputValue(stockL) +
      getInputValue(stockXL) +
      getInputValue(stockXXL);

    if (modalTotal) {
      modalTotal.textContent = total;
    }

    return total;
  }


  /* =========================================================
     INPUT VALIDATION
  ========================================================= */

  function normalizeStockInput(input) {

    if (!input) {
      return;
    }

    let value = parseInt(
      input.value,
      10
    );

    if (Number.isNaN(value) || value < 0) {
      value = 0;
    }

    input.value = value;

    calculateModalTotal();
  }


  [stockM, stockL, stockXL, stockXXL]
    .forEach((input) => {

      if (!input) {
        return;
      }

      input.addEventListener(
        "input",
        () => {
          normalizeStockInput(input);
        }
      );

      input.addEventListener(
        "change",
        () => {
          normalizeStockInput(input);
        }
      );

    });


  /* =========================================================
     OPEN MODAL
  ========================================================= */

  function openStockModal(button) {

    if (!button || !modal) {
      return;
    }

    activeProductId =
      button.dataset.productId || null;


    activeProductRow =
      document.querySelector(
        `.inventory-row[data-product-id="${activeProductId}"]`
      );


    activeMobileCard =
      document.querySelector(
        `.inventory-mobile-card[data-product-id="${activeProductId}"]`
      );


    const productName =
      button.dataset.productName || "Product";


    const valueM =
      parseInt(
        button.dataset.stockM || "0",
        10
      ) || 0;

    const valueL =
      parseInt(
        button.dataset.stockL || "0",
        10
      ) || 0;

    const valueXL =
      parseInt(
        button.dataset.stockXl || "0",
        10
      ) || 0;

    const valueXXL =
      parseInt(
        button.dataset.stockXxl || "0",
        10
      ) || 0;


    modalProductName.textContent =
      productName;


    stockM.value = valueM;
    stockL.value = valueL;
    stockXL.value = valueXL;
    stockXXL.value = valueXXL;


    calculateModalTotal();


    modal.classList.add("is-open");

    modal.setAttribute(
      "aria-hidden",
      "false"
    );

    document.body.classList.add(
      "inventory-modal-open"
    );


    setTimeout(() => {

      if (stockM) {
        stockM.focus();
      }

    }, 100);

  }


  /* =========================================================
     CLOSE MODAL
  ========================================================= */

  function closeStockModal() {

    if (!modal) {
      return;
    }

    modal.classList.remove(
      "is-open"
    );

    modal.setAttribute(
      "aria-hidden",
      "true"
    );

    document.body.classList.remove(
      "inventory-modal-open"
    );

    activeProductId = null;
    activeProductRow = null;
    activeMobileCard = null;

  }


  /* =========================================================
     MANAGE BUTTONS
  ========================================================= */

  function bindManageButtons() {

    const buttons =
      document.querySelectorAll(
        ".inventory-manage-btn"
      );


    buttons.forEach((button) => {

      button.addEventListener(
        "click",
        () => {
          openStockModal(button);
        }
      );

    });

  }


  bindManageButtons();


  /* =========================================================
     UPDATE TABLE ROW
  ========================================================= */

  function updateTableRow(
    row,
    data
  ) {

    if (!row) {
      return;
    }


    const sizeM =
      row.querySelector(
        '[data-size="M"]'
      );

    const sizeL =
      row.querySelector(
        '[data-size="L"]'
      );

    const sizeXL =
      row.querySelector(
        '[data-size="XL"]'
      );

    const sizeXXL =
      row.querySelector(
        '[data-size="XXL"]'
      );

    const totalElement =
      row.querySelector(
        "[data-total]"
      );

    const statusElement =
      row.querySelector(
        ".inventory-status"
      );

    const updatedElement =
      row.querySelector(
        ".inventory-updated"
      );


    if (sizeM) {
      sizeM.textContent = data.M;
    }

    if (sizeL) {
      sizeL.textContent = data.L;
    }

    if (sizeXL) {
      sizeXL.textContent = data.XL;
    }

    if (sizeXXL) {
      sizeXXL.textContent = data.XXL;
    }


    if (totalElement) {
      totalElement.textContent =
        data.total;
    }


    if (statusElement) {

      statusElement.className =
        "inventory-status";

      statusElement.classList.add(
        `status-${data.status}`
      );

      statusElement.textContent =
        getStatusLabel(
          data.status
        );

    }


    if (updatedElement) {

      updatedElement.textContent =
        data.updated_at;

    }


    row.dataset.status =
      data.status;

    row.dataset.total =
      data.total;


    /* -------------------------------------------------------
       Update manage button
    ------------------------------------------------------- */

    const manageButton =
      row.querySelector(
        ".inventory-manage-btn"
      );

    if (manageButton) {

      manageButton.dataset.stockM =
        data.M;

      manageButton.dataset.stockL =
        data.L;

      manageButton.dataset.stockXl =
        data.XL;

      manageButton.dataset.stockXxl =
        data.XXL;

    }

  }


  /* =========================================================
     UPDATE MOBILE CARD
  ========================================================= */

  function updateMobileCard(
    card,
    data
  ) {

    if (!card) {
      return;
    }


    const stockItems =
      card.querySelectorAll(
        ".mobile-stock-item"
      );


    /*
      Order:

      0 = M
      1 = L
      2 = XL
      3 = XXL
      4 = Total
    */

    if (stockItems.length >= 5) {

      const values = [
        data.M,
        data.L,
        data.XL,
        data.XXL,
        data.total
      ];


      values.forEach(
        (value, index) => {

          const strong =
            stockItems[index]
              .querySelector("strong");

          if (strong) {
            strong.textContent =
              value;
          }

        }
      );

    }


    /* -------------------------------------------------------
       Status
    ------------------------------------------------------- */

    const statusElement =
      card.querySelector(
        ".inventory-status"
      );

    if (statusElement) {

      statusElement.className =
        "inventory-status";

      statusElement.classList.add(
        `status-${data.status}`
      );

      statusElement.textContent =
        getStatusLabel(
          data.status
        );

    }


    /* -------------------------------------------------------
       Update button
    ------------------------------------------------------- */

    const manageButton =
      card.querySelector(
        ".inventory-manage-btn"
      );

    if (manageButton) {

      manageButton.dataset.stockM =
        data.M;

      manageButton.dataset.stockL =
        data.L;

      manageButton.dataset.stockXl =
        data.XL;

      manageButton.dataset.stockXxl =
        data.XXL;

    }


    card.dataset.status =
      data.status;

    card.dataset.total =
      data.total;

  }


  /* =========================================================
     UPDATE SUMMARY COUNTS
  ========================================================= */

  function updateSummaryCounts() {

    const rows =
      document.querySelectorAll(
        ".inventory-row"
      );


    let inStock = 0;
    let lowStock = 0;
    let outOfStock = 0;


    rows.forEach((row) => {

      if (
        row.style.display === "none"
      ) {
        return;
      }


      const status =
        row.dataset.status;


      if (status === "in-stock") {
        inStock++;
      }

      else if (status === "low-stock") {
        lowStock++;
      }

      else if (status === "out-of-stock") {
        outOfStock++;
      }

    });


    const totalElement =
      document.getElementById(
        "totalProductsCount"
      );

    const inStockElement =
      document.getElementById(
        "inStockCount"
      );

    const lowStockElement =
      document.getElementById(
        "lowStockCount"
      );

    const outOfStockElement =
      document.getElementById(
        "outOfStockCount"
      );


    /*
      Total products should represent
      all products, not only filtered rows.
    */

    if (totalElement) {

      totalElement.textContent =
        rows.length;

    }


    if (inStockElement) {

      inStockElement.textContent =
        inStock;

    }


    if (lowStockElement) {

      lowStockElement.textContent =
        lowStock;

    }


    if (outOfStockElement) {

      outOfStockElement.textContent =
        outOfStock;

    }

  }


  /* =========================================================
     FILTER INVENTORY
  ========================================================= */

  function filterInventory() {

    const search =
      searchInput
        ? searchInput.value
            .trim()
            .toLowerCase()
        : "";


    const stockStatus =
      stockFilter
        ? stockFilter.value
        : "all";


    const category =
      categoryFilter
        ? categoryFilter.value
        : "all";


    let visibleCount = 0;


    /* -------------------------------------------------------
       TABLE ROWS
    ------------------------------------------------------- */

    const rows =
      document.querySelectorAll(
        ".inventory-row"
      );


    rows.forEach((row) => {

      const name =
        row.dataset.productName || "";

      const code =
        row.dataset.productCode || "";

      const rowCategory =
        row.dataset.category || "";

      const status =
        row.dataset.status || "";


      const searchMatch =
        !search ||
        name.includes(search) ||
        code.includes(search);


      const statusMatch =
        stockStatus === "all" ||
        status === stockStatus;


      const categoryMatch =
        category === "all" ||
        rowCategory === category;


      const visible =
        searchMatch &&
        statusMatch &&
        categoryMatch;


      row.style.display =
        visible ? "" : "none";


      if (visible) {
        visibleCount++;
      }

    });


    /* -------------------------------------------------------
       MOBILE CARDS
    ------------------------------------------------------- */

    const cards =
      document.querySelectorAll(
        ".inventory-mobile-card"
      );


    cards.forEach((card) => {

      const name =
        card.dataset.productName || "";

      const code =
        card.dataset.productCode || "";

      const cardCategory =
        card.dataset.category || "";

      const status =
        card.dataset.status || "";


      const searchMatch =
        !search ||
        name.includes(search) ||
        code.includes(search);


      const statusMatch =
        stockStatus === "all" ||
        status === stockStatus;


      const categoryMatch =
        category === "all" ||
        cardCategory === category;


      const visible =
        searchMatch &&
        statusMatch &&
        categoryMatch;


      card.style.display =
        visible ? "" : "none";

    });


    /* -------------------------------------------------------
       Empty State
    ------------------------------------------------------- */

    if (emptyState) {

      emptyState.style.display =
        visibleCount === 0
          ? "block"
          : "none";

    }

  }


  /* =========================================================
     SEARCH EVENTS
  ========================================================= */

  if (searchInput) {

    searchInput.addEventListener(
      "input",
      filterInventory
    );

  }


  if (stockFilter) {

    stockFilter.addEventListener(
      "change",
      filterInventory
    );

  }


  if (categoryFilter) {

    categoryFilter.addEventListener(
      "change",
      filterInventory
    );

  }


  /* =========================================================
     SAVE STOCK TO DATABASE
  ========================================================= */

  async function saveStock() {

    if (!activeProductId) {

      alert(
        "No product selected."
      );

      return;

    }


    /* -------------------------------------------------------
       Get values
    ------------------------------------------------------- */

    const valueM =
      getInputValue(stockM);

    const valueL =
      getInputValue(stockL);

    const valueXL =
      getInputValue(stockXL);

    const valueXXL =
      getInputValue(stockXXL);


    const total =
      valueM +
      valueL +
      valueXL +
      valueXXL;


    /* -------------------------------------------------------
       Disable button
    ------------------------------------------------------- */

    if (modalSave) {

      modalSave.disabled = true;

      modalSave.dataset.originalText =
        modalSave.innerHTML;

      modalSave.innerHTML = `
        <i class="bi bi-arrow-repeat"></i>
        <span>Saving...</span>
      `;

    }


    /* -------------------------------------------------------
       Form Data
    ------------------------------------------------------- */

    const formData =
      new FormData();


    formData.append(
      "product_id",
      activeProductId
    );

    formData.append(
      "stock_M",
      valueM
    );

    formData.append(
      "stock_L",
      valueL
    );

    formData.append(
      "stock_XL",
      valueXL
    );

    formData.append(
      "stock_XXL",
      valueXXL
    );


    /* -------------------------------------------------------
       Send request
    ------------------------------------------------------- */

    try {

      const response =
        await fetch(
          "/admin/inventory/update-stock/",
          {
            method: "POST",

            headers: {
              "X-CSRFToken":
                getCSRFToken(),

              "X-Requested-With":
                "XMLHttpRequest"
            },

            body: formData
          }
        );


      let data;


      try {

        data =
          await response.json();

      }

      catch (error) {

        throw new Error(
          "Invalid server response."
        );

      }


      /* -----------------------------------------------------
         Backend error
      ----------------------------------------------------- */

      if (
        !response.ok ||
        !data.success
      ) {

        throw new Error(
          data.message ||
          "Unable to update stock."
        );

      }


      /* -----------------------------------------------------
         Update table
      ----------------------------------------------------- */

      updateTableRow(
        activeProductRow,
        data
      );


      /* -----------------------------------------------------
         Update mobile
      ----------------------------------------------------- */

      updateMobileCard(
        activeMobileCard,
        data
      );


      /* -----------------------------------------------------
         Update modal total
      ----------------------------------------------------- */

      if (modalTotal) {

        modalTotal.textContent =
          data.total;

      }


      /* -----------------------------------------------------
         Update summary
      ----------------------------------------------------- */

      updateSummaryCounts();


      /* -----------------------------------------------------
         Re-apply filters
      ----------------------------------------------------- */

      filterInventory();


      /* -----------------------------------------------------
         Close modal
      ----------------------------------------------------- */

      closeStockModal();


      /* -----------------------------------------------------
         Success message
      ----------------------------------------------------- */

      showInventoryMessage(
        "Stock updated successfully.",
        "success"
      );

    }

    catch (error) {

      console.error(
        "Inventory update error:",
        error
      );


      showInventoryMessage(
        error.message ||
          "Failed to update stock.",
        "error"
      );

    }

    finally {

      if (modalSave) {

        modalSave.disabled = false;

        modalSave.innerHTML =
          modalSave.dataset.originalText ||
          `
            <i class="bi bi-check2"></i>
            <span>Save Stock</span>
          `;

      }

    }

  }


  /* =========================================================
     SAVE BUTTON
  ========================================================= */

  if (modalSave) {

    modalSave.addEventListener(
      "click",
      saveStock
    );

  }


  /* =========================================================
     CLOSE EVENTS
  ========================================================= */

  if (modalClose) {

    modalClose.addEventListener(
      "click",
      closeStockModal
    );

  }


  if (modalCancel) {

    modalCancel.addEventListener(
      "click",
      closeStockModal
    );

  }


  if (modalOverlay) {

    modalOverlay.addEventListener(
      "click",
      closeStockModal
    );

  }


  /* =========================================================
     ESC KEY
  ========================================================= */

  document.addEventListener(
    "keydown",
    (event) => {

      if (
        event.key === "Escape" &&
        modal &&
        modal.classList.contains(
          "is-open"
        )
      ) {

        closeStockModal();

      }

    }
  );


  /* =========================================================
     REFRESH
  ========================================================= */

  if (refreshButton) {

    refreshButton.addEventListener(
      "click",
      () => {

        refreshButton.classList.add(
          "is-loading"
        );

        refreshButton.disabled = true;


        /*
          Reload page so inventory data
          comes directly from database.
        */

        setTimeout(() => {

          window.location.reload();

        }, 350);

      }
    );

  }


  /* =========================================================
     MESSAGE
  ========================================================= */

  function showInventoryMessage(
    message,
    type = "success"
  ) {

    /*
      Remove previous message.
    */

    const existing =
      document.querySelector(
        ".inventory-toast"
      );

    if (existing) {
      existing.remove();
    }


    const toast =
      document.createElement(
        "div"
      );


    toast.className =
      "inventory-toast";


    if (type === "error") {

      toast.classList.add(
        "inventory-toast-error"
      );

    }


    toast.innerHTML = `
      <i class="bi ${
        type === "error"
          ? "bi-x-circle"
          : "bi-check-circle"
      }"></i>

      <span>${message}</span>
    `;


    document.body.appendChild(
      toast
    );


    requestAnimationFrame(() => {

      toast.classList.add(
        "show"
      );

    });


    setTimeout(() => {

      toast.classList.remove(
        "show"
      );


      setTimeout(() => {

        toast.remove();

      }, 250);

    }, 2500);

  }


  /* =========================================================
     TOAST CSS
  ========================================================= */

  const toastStyle =
    document.createElement(
      "style"
    );


  toastStyle.textContent = `
    .inventory-toast {
      position: fixed;
      right: 20px;
      bottom: 20px;
      z-index: 10001;

      min-height: 38px;
      max-width: 300px;

      padding: 0 13px;

      display: flex;
      align-items: center;
      gap: 8px;

      border: 1px solid #2d2d2d;
      border-radius: 6px;

      background: #111111;
      color: #cfcfcf;

      font-family: "Poppins", sans-serif;
      font-size: 9px;
      font-weight: 400;

      box-shadow:
        0 12px 35px rgba(0, 0, 0, 0.45);

      opacity: 0;
      transform: translateY(8px);

      transition:
        opacity 0.2s ease,
        transform 0.2s ease;
    }

    .inventory-toast.show {
      opacity: 1;
      transform: translateY(0);
    }

    .inventory-toast i {
      font-size: 11px;
      color: #bdbdbd;
    }

    .inventory-toast-error i {
      color: #858585;
    }

    @media (max-width: 500px) {
      .inventory-toast {
        right: 10px;
        left: 10px;
        bottom: 10px;
        max-width: none;
      }
    }
  `;


  document.head.appendChild(
    toastStyle
  );


  /* =========================================================
     INITIAL FILTER
  ========================================================= */

  filterInventory();

});