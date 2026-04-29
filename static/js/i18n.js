const TRANSLATIONS = {
  uz: {
    nav_submit: "Ariza yuborish", nav_status: "Holat tekshirish", nav_login: "Xodimlar",
    hero_title: "Professional Yuridik Yordam", hero_sub: "Tajribali yuristlar jamoasi sizning huquqiy muammolaringizni hal etishga tayyor.",
    hero_btn: "Ariza yuborish", hero_btn2: "Holat tekshirish",
    form_title: "Ariza yuborish", form_name: "To'liq ism *", form_phone: "Telefon raqami *",
    form_text: "Muammoni tasvirlab bering *", form_file: "Hujjat biriktirish (ixtiyoriy)",
    form_submit: "Ariza yuborish", form_submitting: "Yuborilmoqda...",
    success_title: "Arizangiz qabul qilindi!", success_id: "Ariza raqami:",
    success_msg: "Administrator tez orada ko'rib chiqadi.", success_btn: "Holatni tekshirish",
    status_title: "Ariza holatini tekshirish", status_placeholder: "Ariza raqamini kiriting",
    status_btn: "Tekshirish", status_not_found: "Ariza topilmadi.",
    status_label: "Holat", direction_label: "Yo'nalish", amount_label: "Umumiy summa",
    invoice_label: "Hisob-faktura", pay_btn: "To'lovga o'tish", cabinet_btn: "Kabinetni ochish",
    statuses: {new:"Yangi",reviewing:"Ko'rib chiqilmoqda",offered:"Taklif yuborildi",paid:"To'langan",assigned:"Yurist tayinlandi",closed:"Yopildi"},
    pay_title: "To'lov", pay_demo: "Demo rejim — haqiqiy pul yechilmaydi.",
    pay_req_id: "Ariza raqami", pay_total: "Umumiy summa", pay_invoice: "Hisob-faktura",
    pay_amount: "To'lov miqdori (10%)", pay_status: "Holat", pay_paid: "To'langan",
    pay_pending: "Kutilmoqda", pay_choose: "To'lov usulini tanlang:",
    pay_confirmed: "To'lov tasdiqlandi!", pay_open_cabinet: "Kabinetni ochish",
    pay_wait: "Hisob-faktura tayyorlanmoqda. Iltimos, kuting.",
    cab_case: "Ish ma'lumotlari", cab_id: "Raqam", cab_status: "Holat",
    cab_case_status: "Ish holati", cab_lawyer: "Sizning yuristingiz",
    cab_invoice: "To'lov", cab_paid: "To'langan", cab_chat: "Yurist bilan muloqot",
    cab_placeholder: "Xabar yozing...", cab_send: "Yuborish", cab_file: "Fayl",
    cab_meetings: "Uchrashuvlar", cab_no_meetings: "Hozircha uchrashuv yo'q.",
    meet_online: "Online", meet_office: "Ofisda", meet_confirmed: "Tasdiqlangan",
    meet_pending: "Kutilmoqda", meet_cancelled: "Bekor qilindi", meet_done: "O'tkazildi",
    features: ["Maxfiylik kafolati", "Tajribali yuristlar", "Tez javob", "Onlayn maslahat"],
  },
  ru: {
    nav_submit: "Подать заявку", nav_status: "Проверить статус", nav_login: "Сотрудники",
    hero_title: "Профессиональная юридическая помощь", hero_sub: "Команда опытных юристов готова решить ваши правовые вопросы.",
    hero_btn: "Подать заявку", hero_btn2: "Проверить статус",
    form_title: "Подать заявку", form_name: "Полное имя *", form_phone: "Номер телефона *",
    form_text: "Опишите вашу проблему *", form_file: "Прикрепить документ (необязательно)",
    form_submit: "Отправить заявку", form_submitting: "Отправка...",
    success_title: "Заявка принята!", success_id: "Номер заявки:",
    success_msg: "Администратор рассмотрит её в ближайшее время.", success_btn: "Проверить статус",
    status_title: "Проверить статус заявки", status_placeholder: "Введите номер заявки",
    status_btn: "Проверить", status_not_found: "Заявка не найдена.",
    status_label: "Статус", direction_label: "Направление", amount_label: "Общая сумма",
    invoice_label: "Счёт", pay_btn: "Перейти к оплате", cabinet_btn: "Открыть кабинет",
    statuses: {new:"Новая",reviewing:"На рассмотрении",offered:"Предложение отправлено",paid:"Оплачено",assigned:"Юрист назначен",closed:"Закрыта"},
    pay_title: "Оплата", pay_demo: "Демо режим — реальные деньги не списываются.",
    pay_req_id: "Номер заявки", pay_total: "Общая сумма", pay_invoice: "Счёт",
    pay_amount: "Сумма к оплате (10%)", pay_status: "Статус", pay_paid: "Оплачено",
    pay_pending: "Ожидает оплаты", pay_choose: "Выберите способ оплаты:",
    pay_confirmed: "Оплата подтверждена!", pay_open_cabinet: "Открыть кабинет",
    pay_wait: "Счёт готовится. Пожалуйста, подождите.",
    cab_case: "Информация о деле", cab_id: "Номер", cab_status: "Статус",
    cab_case_status: "Статус дела", cab_lawyer: "Ваш юрист",
    cab_invoice: "Оплата", cab_paid: "Оплачено", cab_chat: "Чат с юристом",
    cab_placeholder: "Напишите сообщение...", cab_send: "Отправить", cab_file: "Файл",
    cab_meetings: "Встречи", cab_no_meetings: "Встреч пока нет.",
    meet_online: "Онлайн", meet_office: "В офисе", meet_confirmed: "Подтверждена",
    meet_pending: "Ожидает", meet_cancelled: "Отменена", meet_done: "Проведена",
    features: ["Гарантия конфиденциальности", "Опытные юристы", "Быстрый ответ", "Онлайн консультация"],
  },
  en: {
    nav_submit: "Submit Request", nav_status: "Check Status", nav_login: "Staff",
    hero_title: "Professional Legal Assistance", hero_sub: "Our team of experienced lawyers is ready to resolve your legal matters.",
    hero_btn: "Submit Request", hero_btn2: "Check Status",
    form_title: "Submit a Request", form_name: "Full Name *", form_phone: "Phone Number *",
    form_text: "Describe your issue *", form_file: "Attach document (optional)",
    form_submit: "Submit Request", form_submitting: "Submitting...",
    success_title: "Request Submitted!", success_id: "Request ID:",
    success_msg: "An administrator will review it shortly.", success_btn: "Check Status",
    status_title: "Check Request Status", status_placeholder: "Enter your request ID",
    status_btn: "Check", status_not_found: "Request not found.",
    status_label: "Status", direction_label: "Direction", amount_label: "Total Amount",
    invoice_label: "Invoice", pay_btn: "Go to Payment", cabinet_btn: "Open Cabinet",
    statuses: {new:"New",reviewing:"Under Review",offered:"Offer Sent",paid:"Paid",assigned:"Lawyer Assigned",closed:"Closed"},
    pay_title: "Payment", pay_demo: "Demo mode — no real money is charged.",
    pay_req_id: "Request ID", pay_total: "Total Amount", pay_invoice: "Invoice",
    pay_amount: "Amount due (10%)", pay_status: "Status", pay_paid: "Paid",
    pay_pending: "Pending", pay_choose: "Choose payment method:",
    pay_confirmed: "Payment confirmed!", pay_open_cabinet: "Open Cabinet",
    pay_wait: "Invoice is being prepared. Please check back soon.",
    cab_case: "Case Information", cab_id: "ID", cab_status: "Status",
    cab_case_status: "Case Status", cab_lawyer: "Your Lawyer",
    cab_invoice: "Payment", cab_paid: "Paid", cab_chat: "Chat with Lawyer",
    cab_placeholder: "Type a message...", cab_send: "Send", cab_file: "File",
    cab_meetings: "Meetings", cab_no_meetings: "No meetings scheduled yet.",
    meet_online: "Online", meet_office: "In Office", meet_confirmed: "Confirmed",
    meet_pending: "Pending", meet_cancelled: "Cancelled", meet_done: "Done",
    features: ["Confidentiality guaranteed", "Experienced lawyers", "Fast response", "Online consultation"],
  }
};

function getLang() { return localStorage.getItem('lf_lang') || 'ru'; }
function setLang(l) { localStorage.setItem('lf_lang', l); location.reload(); }
function tr(key) { return (TRANSLATIONS[getLang()] || TRANSLATIONS['ru'])[key] || key; }

function applyTranslations() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    const attr = el.getAttribute('data-i18n-attr');
    if (attr) el.setAttribute(attr, tr(key));
    else el.textContent = tr(key);
  });
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.lang === getLang());
  });
}

document.addEventListener('DOMContentLoaded', applyTranslations);

function getCookie(name) {
  return document.cookie.split(';').map(c => c.trim()).find(c => c.startsWith(name + '='))?.split('=')[1] || '';
}
