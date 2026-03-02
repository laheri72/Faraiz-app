export const formatCurrencyIndian = (num: number): string => {
    const x = num.toString();
    let lastThree = x.substring(x.length - 3);
    const otherNumbers = x.substring(0, x.length - 3);
    if (otherNumbers !== '') {
        lastThree = ',' + lastThree;
    }
    const res = otherNumbers.replace(/\B(?=(\d{2})+(?!\d))/g, ",") + lastThree;
    return res;
};

export const numberToWords = (numValue: number): string => {
    const a = ['', 'One ', 'Two ', 'Three ', 'Four ', 'Five ', 'Six ', 'Seven ', 'Eight ', 'Nine ', 'Ten ', 'Eleven ', 'Twelve ', 'Thirteen ', 'Fourteen ', 'Fifteen ', 'Sixteen ', 'Seventeen ', 'Eighteen ', 'Nineteen '];
    const b = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety'];

    if (numValue === 0) return 'Zero';
    const numStr = numValue.toString();
    if (numStr.length > 9) return 'Overflow';
    
    const n = ('000000000' + numStr).slice(-9).match(/^(\d{2})(\d{2})(\d{2})(\d{1})(\d{2})$/);
    if (!n) return ''; 
    
    let str = '';
    
    const parsePart = (valStr: string) => parseInt(valStr, 10);

    str += (parsePart(n[1]) !== 0) ? (a[parsePart(n[1])] || b[parsePart(n[1][0])] + ' ' + a[parsePart(n[1][1])]) + 'Crore ' : '';
    str += (parsePart(n[2]) !== 0) ? (a[parsePart(n[2])] || b[parsePart(n[2][0])] + ' ' + a[parsePart(n[2][1])]) + 'Lakh ' : '';
    str += (parsePart(n[3]) !== 0) ? (a[parsePart(n[3])] || b[parsePart(n[3][0])] + ' ' + a[parsePart(n[3][1])]) + 'Thousand ' : '';
    str += (parsePart(n[4]) !== 0) ? (a[parsePart(n[4])] || b[parsePart(n[4][0])] + ' ' + a[parsePart(n[4][1])]) + 'Hundred ' : '';
    str += (parsePart(n[5]) !== 0) ? ((str !== '') ? 'and ' : '') + (a[parsePart(n[5])] || b[parsePart(n[5][0])] + ' ' + a[parsePart(n[5][1])]) : '';
    
    return str.trim() + ' Units';
};
