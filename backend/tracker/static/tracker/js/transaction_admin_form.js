// JS шаблон, который обеспечивает динамическое обновление выпадающих списков в форме транзакций

document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM полностью загружен. Начинаем поиск элементов.");

  const typeSelect = document.querySelector("#id_type");
  const categorySelect = document.querySelector("#id_category");
  const subcategorySelect = document.querySelector("#id_subcategory");
  const saveButton = document.querySelector('input[name="_save"]');

  if (!typeSelect || !categorySelect || !subcategorySelect || !saveButton) {
    console.error(
      "Один из ключевых элементов (select или кнопка 'Сохранить') не найден!"
    );
    return;
  }
  console.log("Все select-элементы и кнопка 'Сохранить' успешно найдены.");

  const DJANGO_PLACEHOLDER = "---------";

  const categoryUrl = "/api/get-categories/";
  const subcategoryUrl = "/api/get-subcategories/";

  function validateForm() {
    const isTypeSelected = typeSelect.value !== "";
    const isCategorySelected = categorySelect.value !== "";
    const isSubcategorySelected = subcategorySelect.value !== "";

    if (isTypeSelected && isCategorySelected && isSubcategorySelected) {
      saveButton.disabled = false;
      saveButton.classList.remove("disabled");
    } else {
      saveButton.disabled = true;
      saveButton.classList.add("disabled");
    }
  }

  function updateSelect(selectElement, options, placeholder) {
    const selectedValue = selectElement.value;
    selectElement.innerHTML = "";

    const placeholderOption = document.createElement("option");
    placeholderOption.value = "";
    placeholderOption.textContent = placeholder || DJANGO_PLACEHOLDER;
    selectElement.appendChild(placeholderOption);

    options.forEach(function (optionData) {
      const option = document.createElement("option");
      option.value = optionData.id;
      option.textContent = optionData.name;
      selectElement.appendChild(option);
    });

    if (options.some((option) => option.id == selectedValue)) {
      selectElement.value = selectedValue;
    } else {
      selectElement.value = "";
    }
    validateForm();
  }

  function resetSelect(selectElement, placeholder) {
    selectElement.innerHTML = "";
    const placeholderOption = document.createElement("option");
    placeholderOption.value = "";
    placeholderOption.textContent = placeholder || DJANGO_PLACEHOLDER;
    selectElement.appendChild(placeholderOption);
    validateForm();
  }

  typeSelect.addEventListener("change", function () {
    const typeId = this.value;
    resetSelect(categorySelect);
    resetSelect(subcategorySelect);

    if (typeId) {
      const url = `${categoryUrl}?type_id=${typeId}`;
      fetch(url)
        .then((response) =>
          response.ok ? response.json() : Promise.reject(response)
        )
        .then((data) => {
          updateSelect(categorySelect, data);
          categorySelect.dispatchEvent(new Event("change"));
        })
        .catch((error) => {
          console.error("Ошибка Fetch-запроса для категорий:", error);
          resetSelect(categorySelect);
        });
    } else {
      categorySelect.dispatchEvent(new Event("change"));
    }
  });

  categorySelect.addEventListener("change", function () {
    const categoryId = this.value;
    resetSelect(subcategorySelect);

    if (categoryId) {
      const url = `${subcategoryUrl}?category_id=${categoryId}`;
      fetch(url)
        .then((response) =>
          response.ok ? response.json() : Promise.reject(response)
        )
        .then((data) => {
          updateSelect(subcategorySelect, data);
        })
        .catch((error) => {
          console.error("Ошибка Fetch-запроса для подкатегорий:", error);
          resetSelect(subcategorySelect);
        });
    }
  });

  subcategorySelect.addEventListener("change", validateForm);

  validateForm();

  console.log("Все обработчики событий установлены.");
});
