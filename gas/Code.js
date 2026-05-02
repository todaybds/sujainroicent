// ==========================================
// 인하대역 수자인 로이센트 — CRM Apps Script
//
// [핵심 동작]
//   1. doPost — Vercel /api/register로부터 호출 → "콜" 시트에 행 추가 + 이메일 알림
//   2. onLeadUpdated — 5분 트리거로 빈 "구분" 컬럼에 자동 ID 채번
//   3. setupSpreadsheet — 최초 1회 실행, "콜" 시트 헤더 설정
//
// [배포]
//   웹앱 > 실행 주체: 나 > 액세스: 모든 사용자(또는 익명)
//   배포 후 받은 /exec URL을 Vercel 환경변수 GAS_FORM_URL에 입력
//
// [콜 시트 열 구조] 1행 헤더, 2행부터 데이터
//   A 구분  B 등록일  C 경로  D 고객명
//   E 전화번호  F 방문예약  G 예약시간
//   H 연령대  I 성별  J 거주지역
//   K 내용  L 담당자  M 상태
//   N utm_source  O utm_medium  P utm_campaign  Q utm_term
//   R IP주소  S 접속기기  T 알림  U 비고  V Meta전송
// ==========================================

var SITE_NAME = "인하대역 수자인 로이센트";
var ADMIN_EMAIL = "skrl1347@gmail.com";


// ==========================================
// 시트 초기 세팅 (최초 1회 실행)
// ==========================================
function setupSpreadsheet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  ss.rename(SITE_NAME);
  setupCallSheet_(ss);
  var sheets = ss.getSheets();
  for (var i = 0; i < sheets.length; i++) {
    var nm = sheets[i].getName();
    if ((nm === "Sheet1" || nm === "시트1") && ss.getSheets().length > 1) {
      ss.deleteSheet(sheets[i]);
    }
  }
  SpreadsheetApp.getUi().alert("✅ 초기 세팅 완료!\n\n콜 시트가 준비되었습니다.");
}

function setupCallSheet_(ss) {
  var ws = ss.getSheetByName("콜") || ss.insertSheet("콜");
  ws.clear(); ws.setTabColor("#5B8DEF");
  var headers = [
    {n:"구분",w:50,c:"#1E3A5F"},{n:"등록일",w:120,c:"#1E3A5F"},{n:"경로",w:80,c:"#1E3A5F"},{n:"고객명",w:80,c:"#1E3A5F"},
    {n:"전화번호",w:120,c:"#2E6B4F"},{n:"방문예약",w:100,c:"#2E6B4F"},{n:"예약시간",w:80,c:"#2E6B4F"},
    {n:"연령대",w:60,c:"#5B4A7A"},{n:"성별",w:45,c:"#5B4A7A"},{n:"거주지역",w:75,c:"#5B4A7A"},
    {n:"내용",w:450,c:"#1E3A5F"},{n:"담당자",w:80,c:"#1E3A5F"},{n:"상태",w:80,c:"#1E3A5F"},
    {n:"utm_source",w:85,c:"#7A5B2E"},{n:"utm_medium",w:75,c:"#7A5B2E"},{n:"utm_campaign",w:140,c:"#7A5B2E"},{n:"utm_term",w:110,c:"#7A5B2E"},
    {n:"IP 주소",w:180,c:"#4A4A4A"},{n:"접속기기",w:75,c:"#4A4A4A"},
    {n:"알림",w:70,c:"#4A4A4A"},{n:"비고",w:80,c:"#4A4A4A"},{n:"Meta전송",w:100,c:"#4A4A4A"},
  ];
  ws.getRange(1, 1, 1, headers.length).setValues([headers.map(function(h){return h.n;})]);
  headers.forEach(function(h, i) {
    ws.getRange(1, i+1).setBackground(h.c).setFontColor("#F0F0F0")
      .setFontFamily("맑은 고딕").setFontSize(9).setFontWeight("bold")
      .setHorizontalAlignment("center").setVerticalAlignment("middle");
    ws.setColumnWidth(i+1, h.w);
  });
  ws.setRowHeight(1, 30);
  ws.getRange("A2:V200").setFontFamily("맑은 고딕").setFontSize(9).setFontColor("#333333")
    .setVerticalAlignment("middle").setWrapStrategy(SpreadsheetApp.WrapStrategy.WRAP);
  var statusVal = SpreadsheetApp.newDataValidation()
    .requireValueInList(["부재","미정","예약","예약취소","내방","고려","계약","이탈","업무방해의심"], true)
    .setAllowInvalid(false).build();
  ws.getRange("M2:M200").setDataValidation(statusVal);
  ws.setFrozenRows(1); ws.getRange("A1:V1").createFilter();
}


// ==========================================
// 트리거 셋업 (최초 1회 실행)
// ==========================================
function setupAllTriggers() {
  ScriptApp.getProjectTriggers().forEach(function(t) {
    if (t.getHandlerFunction() === "onLeadUpdated") ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger("onLeadUpdated").timeBased().everyMinutes(5).create();
  Logger.log("✅ onLeadUpdated 5분 트리거 등록 완료");
}


// ==========================================
// 자동 ID 부여 (5분 트리거)
// ==========================================
function getNextId_(callSheet) {
  var lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    var lastRow = callSheet.getLastRow();
    var maxId = 0;
    if (lastRow >= 2) {
      var ids = callSheet.getRange(2, 1, lastRow - 1, 1).getValues();
      for (var i = 0; i < ids.length; i++) {
        if (ids[i][0] && !isNaN(ids[i][0])) maxId = Math.max(maxId, Number(ids[i][0]));
      }
    }
    return maxId + 1;
  } finally {
    lock.releaseLock();
  }
}

function onLeadUpdated() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName("콜");
  if (!sheet) return;
  var lastRow = sheet.getLastRow();
  if (lastRow < 2) return;
  var range = sheet.getRange(2, 1, lastRow - 1, 1);
  var ids = range.getValues();
  for (var i = 0; i < ids.length; i++) {
    if (!ids[i][0] && sheet.getRange(i + 2, 4).getValue()) {
      var nextId = getNextId_(sheet);
      sheet.getRange(i + 2, 1).setValue(nextId);
    }
  }
}


// ==========================================
// 유틸
// ==========================================
function normalizePhone_(p) {
  if (!p) return "";
  var s = p.toString().replace(/[^0-9]/g, "");
  if (s.startsWith("8210")) s = "0" + s.substring(2);
  if (s.startsWith("0010")) s = "010" + s.substring(4);
  if (s.length === 11) return s.substr(0,3) + "-" + s.substr(3,4) + "-" + s.substr(7,4);
  return p;
}

function _formatDateWithDay(dt) {
  if (!dt) return "";
  var s = String(dt).trim();
  var m = s.match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (!m) return s;
  var d = new Date(+m[1], +m[2] - 1, +m[3]);
  var days = ["일요일","월요일","화요일","수요일","목요일","금요일","토요일"];
  return m[1] + "-" + m[2] + "-" + m[3] + " " + days[d.getDay()];
}

function _formatTimeKorean(t) {
  if (!t) return "";
  var s = String(t).trim();
  if (s.indexOf("오전") !== -1 || s.indexOf("오후") !== -1) return s;
  var hm = s.match(/^(\d{1,2}):(\d{2})/);
  if (hm) {
    var h = parseInt(hm[1]), min = hm[2];
    var period = h < 12 ? "오전" : "오후";
    var h12 = h === 0 ? 12 : (h > 12 ? h - 12 : h);
    return min === "00" ? period + " " + h12 + "시" : period + " " + h12 + "시 " + min + "분";
  }
  return s;
}

function _jsonResp(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}


// ==========================================
// [관심고객등록 API] doPost — Vercel API에서 호출
// 시트 저장 + 이메일 알림
// 배포: 웹앱 > 실행 주체: 나 > 액세스: 모든 사용자
// ==========================================
function doPost(e) {
  try {
    var p = JSON.parse(e.postData.contents);
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var sheet = ss.getSheetByName("콜");

    // 자동 셋업: 콜 시트가 없으면 헤더 만들고, 트리거가 없으면 등록
    if (!sheet) {
      setupCallSheet_(ss);
      sheet = ss.getSheetByName("콜");
    }
    var hasTrigger = ScriptApp.getProjectTriggers().some(function(t){
      return t.getHandlerFunction() === 'onLeadUpdated';
    });
    if (!hasTrigger) {
      try { ScriptApp.newTrigger("onLeadUpdated").timeBased().everyMinutes(5).create(); } catch(te) {}
    }

    // 시트에 행 추가
    var row = [
      "",                              // A: 구분 (onLeadUpdated가 자동 부여)
      p.reg_datetime || "",            // B: 등록일
      "관심고객",                       // C: 경로
      p.name || "",                    // D: 고객명
      normalizePhone_(p.phone || ""),  // E: 전화번호
      p.date || "",                    // F: 방문예약
      p.time || "",                    // G: 예약시간
      "", "", "", "",                  // H~K: 연령대/성별/거주지역/내용 (수동)
      "", "",                          // L~M: 담당자/상태 (수동)
      p.utm_source || "",              // N
      p.utm_medium || "",              // O
      p.utm_campaign || "",            // P
      p.utm_term || "",                // Q
      p.ip_address || "",              // R
      p.device || "",                  // S
      ""                               // T: 알림 (이메일 결과 후 채움)
    ];
    sheet.appendRow(row);
    var rowIdx = sheet.getLastRow();

    // 이메일 알림
    var emailSent = false;
    try {
      var subject = "[ " + SITE_NAME + " ] " + (p.name || "") + "님이 양식을 제출하였습니다";
      var body = "이름: " + (p.name || "") +
                 "\n연락처: " + normalizePhone_(p.phone || "") +
                 "\n방문예약일: " + _formatDateWithDay(p.date) +
                 "\n방문시간: " + _formatTimeKorean(p.time);
      if (p.suspect_flag) body += "\n\n🚨 " + p.suspect_flag;
      if (p.recaptcha_score != null) body += "\nreCAPTCHA 점수: " + p.recaptcha_score;
      body += "\n\n──────────────────\n\n" +
              "utm_source: " + (p.utm_source || "") +
              "\nutm_medium: " + (p.utm_medium || "") +
              "\nutm_campaign: " + (p.utm_campaign || "") +
              "\nutm_term: " + (p.utm_term || "") +
              "\ndevice: " + (p.device || "") +
              "\nip: " + (p.ip_address || "");
      MailApp.sendEmail({ to: ADMIN_EMAIL, subject: subject, body: body });
      emailSent = true;
    } catch(em) {}

    sheet.getRange(rowIdx, 20).setValue(emailSent ? "이메일발송" : "이메일실패");

    return _jsonResp({ success: true, email_sent: emailSent });
  } catch(err) {
    return _jsonResp({ error: "서버 오류: " + err.message, code: 500 });
  }
}


// ==========================================
// 테스트용 — 에디터에서 직접 실행
// ==========================================
function _testDoPost() {
  var sample = {
    postData: { contents: JSON.stringify({
      site_domain: "sujainroicent.com",
      name: "테스트", phone: "010-1234-5678",
      date: "2026-05-10", time: "14:00",
      reg_datetime: "2026-05-02 16:30",
      utm_source: "naver", utm_medium: "sa",
      utm_campaign: "test", utm_term: "인하대역수자인",
      ip_address: "127.0.0.1", device: "Desktop"
    })}
  };
  var r = doPost(sample);
  Logger.log(r.getContent());
}
