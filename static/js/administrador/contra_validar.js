document.addEventListener("DOMContentLoaded", () => {
  const pass1 = document.getElementById("id_new_password1");
  const pass2 = document.getElementById("id_new_password2");

  const ruleLength = document.getElementById("rule-length");
  const ruleNumbers = document.getElementById("rule-numbers");
  const ruleMatch = document.getElementById("rule-match");

  function updateRules() {
    const val = pass1.value;

    // longitud
    const lenOk = val.length >= 8;
    ruleLength.textContent = (lenOk ? "✅" : "❌") + " Mínimo 8 caracteres";
    ruleLength.style.color = lenOk ? "#16a34a" : "#dc2626";

    // no solo números
    const numOk = !/^\d+$/.test(val);
    ruleNumbers.textContent = (numOk ? "✅" : "❌") + " No solo números";
    ruleNumbers.style.color = numOk ? "#16a34a" : "#dc2626";

    // match
    const matchOk = val && val === pass2.value;
    ruleMatch.textContent = (matchOk ? "✅" : "❌") + " Las contraseñas coinciden";
    ruleMatch.style.color = matchOk ? "#16a34a" : "#dc2626";
  }

  pass1.addEventListener("input", updateRules);
  pass2.addEventListener("input", updateRules);
});