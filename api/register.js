import nodemailer from 'nodemailer';

const SPREADSHEET_ID = "1bYZ7gm7kDMB5zPdg88Hw8l078-zY7KYC9KBzdG8gBeg";
const NOTIFY_EMAIL = "skrl1347@gmail.com";
const DISPLAY_NAME = "인하대역 수자인 로이센트";
const SITE_DOMAIN = "sujainroicent.com";

function formatDateWithDay(dt) {
  if (!dt) return "";
  const m = String(dt).match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (!m) return String(dt);
  const d = new Date(+m[1], +m[2] - 1, +m[3]);
  const days = ["일요일","월요일","화요일","수요일","목요일","금요일","토요일"];
  return `${m[1]}-${m[2]}-${m[3]} ${days[d.getDay()]}`;
}

function formatTimeKorean(t) {
  if (!t) return "";
  const hm = String(t).match(/^(\d{1,2}):(\d{2})/);
  if (!hm) return String(t);
  const h = parseInt(hm[1]), min = hm[2];
  const period = h < 12 ? "오전" : "오후";
  const h12 = h === 0 ? 12 : (h > 12 ? h - 12 : h);
  return min === "00" ? `${period} ${h12}시` : `${period} ${h12}시 ${min}분`;
}

async function sendEmailFallback(p) {
  if (!process.env.GMAIL_APP_PASSWORD) return;
  const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: { user: NOTIFY_EMAIL, pass: process.env.GMAIL_APP_PASSWORD }
  });
  await transporter.sendMail({
    from: NOTIFY_EMAIL, to: NOTIFY_EMAIL,
    subject: `[ ${DISPLAY_NAME} ] ${p.name || ""}님이 양식을 제출하였습니다`,
    text: `이름: ${p.name}\n연락처: ${p.phone}\n방문예약일: ${formatDateWithDay(p.date)}\n방문시간: ${formatTimeKorean(p.time)}${p.suspect_flag ? '\n\n🚨 ' + p.suspect_flag : ''}${p.recaptcha_score != null ? '\nreCAPTCHA 점수: ' + p.recaptcha_score : ''}\n\n──────────────────\n\nutm_source: ${p.utm_source}\nutm_medium: ${p.utm_medium}\nutm_campaign: ${p.utm_campaign}\nutm_term: ${p.utm_term}\ndevice: ${p.device}\nip: ${p.ip_address}`
  });
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const body = req.body;
  if (body.hp_check && body.hp_check !== "") return res.status(400).json({ error: "봇 감지" });
  if (!body.name || body.name.trim().length < 2) return res.status(400).json({ error: "이름 오류" });

  const phone = body.phone || body.number || "";

  let recaptchaScore = null;
  let suspectFlag = null;
  if (body.recaptcha_token && process.env.RECAPTCHA_SECRET_KEY) {
    try {
      const rcRes = await fetch('https://www.google.com/recaptcha/api/siteverify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `secret=${process.env.RECAPTCHA_SECRET_KEY}&response=${body.recaptcha_token}`
      });
      const rcData = await rcRes.json();
      recaptchaScore = rcData.score ?? null;
      if (rcData.success && rcData.score < 0.3) suspectFlag = '⚠️ reCAPTCHA 저점수: ' + rcData.score;
      if (!rcData.success) suspectFlag = '⚠️ reCAPTCHA 검증실패';
    } catch (e) {}
  } else if (!body.recaptcha_token) {
    suspectFlag = '⚠️ reCAPTCHA 토큰없음';
  }

  const clientIP = (req.headers['x-forwarded-for'] || '').split(',')[0].trim();
  const now = new Date(new Date().getTime() + 9 * 60 * 60 * 1000);
  const formattedDate = now.getUTCFullYear() + '-' +
    String(now.getUTCMonth() + 1).padStart(2, '0') + '-' +
    String(now.getUTCDate()).padStart(2, '0') + ' ' +
    String(now.getUTCHours()).padStart(2, '0') + ':' +
    String(now.getUTCMinutes()).padStart(2, '0');

  const payload = {
    name: body.name.trim(), phone,
    date: body.date || body.visitDate || "",
    time: body.time || body.visitTime || "",
    reg_datetime: formattedDate,
    utm_source: body.utm_source || "", utm_medium: body.utm_medium || "",
    utm_campaign: body.utm_campaign || "", utm_term: body.utm_term || "",
    utm_content: body.utm_content || "",
    ip_address: clientIP, device: body.device || "",
    recaptcha_score: recaptchaScore, suspect_flag: suspectFlag
  };

  try {
    let gasOk = false;
    const errors = [];

    if (process.env.GAS_FORM_URL) {
      try {
        const gasUrl = process.env.GAS_FORM_URL.trim().replace(/\\n/g, '');
        await fetch(gasUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            site_domain: SITE_DOMAIN,
            name: payload.name, phone: payload.phone,
            date: formatDateWithDay(payload.date),
            time: formatTimeKorean(payload.time),
            reg_datetime: formattedDate,
            utm_source: payload.utm_source, utm_medium: payload.utm_medium,
            utm_campaign: payload.utm_campaign, utm_term: payload.utm_term,
            ip_address: payload.ip_address, device: payload.device,
            recaptcha_score: recaptchaScore, suspect_flag: suspectFlag
          }),
          redirect: 'manual'
        });
        gasOk = true;
      } catch (e) { errors.push('gas: ' + e.message); }
    }

    if (!gasOk) {
      try { await sendEmailFallback(payload); } catch (e) { errors.push('email: ' + e.message); }
    }

    return res.status(200).json({ success: true, gas: gasOk, errors });
  } catch (error) {
    console.error("Error:", error);
    return res.status(500).json({ error: "서버 오류" });
  }
}
