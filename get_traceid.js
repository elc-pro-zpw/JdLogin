var window = {};
function t(e, t) {
var n, o, a = parseInt(e, 2),
i = "0",
c = [],
s = Math.pow(2, t) + "";
for (o = s.length - 1; o > -1; o--) n = s[o],
c.push(a * n + "");
for (o = 0; o < c.length; o++) i = r(i, c[o], o);
return i
}
function r(e, t, r) {
var n, o, a;
return o = e.substr(0, e.length - r),
a = e.substr(e.length - r),
n = o / 1 + t / 1,
n + a
}
function n(e, t) {
var r, n, o = 0,
a = [],
i = e.length,
c = t.length,
s = Math.max(i, c);
for (r = 0; r < s; r++)(n = (i - r > 0 ? e.charAt(i - r - 1) / 1 : 0) + (c - r > 0 ? t.charAt(c - r - 1) / 1 : 0) + o) >= 10 ? (o = 1, a.push(n % 10)) : (o = 0, a.push(n));
return a.reverse().join("")
}
 function e() {
var e = {
    bizId: 6,
    operateId: 6
};
var r, o, a, i, c = "",
s = e.operateId,
l = e.bizId,
u = e.isServer || 0,
d = new Date,
m = new Date("2017/01/01"),
p = parseInt((d.getTime() - m.getTime()) / 1e3);
r = 1e3 * parseInt(100 * Math.random()) + d.getMilliseconds();
return r &= 32767,
s &= 2047,
l &= 63,
o = 1073741823 & p,
r = r.toString(2),
s = s.toString(2),
l = l.toString(2),
o = o.toString(2),
r = "000000000000000".substr(0, 15 - r.length) + r,
s = "00000000000".substr(0, 11 - s.length) + s,
l = "000000".substr(0, 6 - l.length) + l,
a = t("0" + o, 33),
i = parseInt(u + l + s + r, 2) + "",
c = n(a, i),
c
}