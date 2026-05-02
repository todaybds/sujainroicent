/**
 * CSV to Table Plugin
 * 1.0.0 최영재
 * CSV 데이터를 HTML 테이블로 삽입합니다.
 * 배열 형태로 csvData와 selector만 넣으면 작동합니다.
 */

class CsvToTable {
    // 생성자: 테이블 배열 받아서 자동 렌더링
    constructor(tables = []) {
        this.tables = tables;
        tables.length > 0 && this.render();
    }

    // 공개 메서드: 테이블 추가 (체이닝 가능)
    add(csvData, selector) {
        this.tables.push({ csvData, selector });
        return this;
    }

    // 공개 메서드: 모든 테이블 렌더링
    render() {
        this.tables.forEach(({ csvData, selector }) => 
            this._renderTable(csvData, selector)
        );
        return this;
    }

    // 공개 메서드: 특정 테이블 초기화
    clear(selector) {
        document.querySelectorAll(selector).forEach(table => {
            const tbody = table.querySelector('tbody');
            tbody && (tbody.innerHTML = '');
        });
        console.log(`🗑️ "${selector}" 초기화 완료`);
        return this;
    }

    // 공개 메서드: 모든 테이블 초기화
    clearAll() {
        this.tables.forEach(({ selector }) => this.clear(selector));
        return this;
    }

    // 내부 메서드: CSV 데이터를 HTML로 변환하여 테이블에 삽입
    _renderTable(csvString, selector) {
        // 1. 테이블 요소 찾기
        const table = document.querySelector(selector);
        if (!table) return console.error(`❌ "${selector}" 테이블을 찾을 수 없습니다`);
        
        const tbody = table.querySelector('tbody');
        if (!tbody) return console.error(`❌ "${selector}" 내에 <tbody>가 없습니다`);

        // 2. CSV 데이터 파싱 (빈 줄 제거)
        const lines = csvString
            .trim()
            .split('\n')
            .filter(line => line.trim());

        if (!lines.length) return console.log(`⚠️ "${selector}": 데이터가 비어있습니다`);

        // 3. HTML 생성 (최적화: map + join)
        const html = lines
            .map(line => {
                const cells = line
                    .split(',')
                    .map(cell => `<td>${this._escape(cell.trim())}</td>`)
                    .join('');
                return `<tr>${cells}</tr>`;
            })
            .join('');

        // 4. DOM 삽입 (한 번에 처리)
        tbody.insertAdjacentHTML('beforeend', html);
        
        console.log(`✅ "${selector}": ${lines.length}개 행 추가 완료`);
    }

    // 내부 메서드: XSS 방어를 위한 HTML 이스케이프
    _escape(text) {
        const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
        return text.replace(/[&<>"']/g, char => map[char]);
    }
}

// 전역 객체로 등록
window.CsvToTable = CsvToTable;
