// 读出 macOS 系统渲染（CoreText，Mac 上的 Safari、Chrome 也用它）眼里每个字的轮廓：
// 每条轮廓的有向面积（正数是逆时针）。CoreText 会按嵌套关系「纠正」轮廓方向，
// 拿它和字体文件里原本的方向一比，就知道哪条轮廓被它当成了字怀。
// 用法：ct_contours <字体文件> <字符…>，每个字输出一行「字符<TAB>面积1 面积2 …」。
import Foundation
import CoreText
import CoreGraphics

let a = CommandLine.arguments
let desc = (CTFontManagerCreateFontDescriptorsFromURL(URL(fileURLWithPath: a[1]) as CFURL) as! [CTFontDescriptor])[0]
let font = CTFontCreateWithFontDescriptor(desc, 1000, nil)

for ch in a[2] {
    var u = Array(String(ch).utf16)
    var g = [CGGlyph](repeating: 0, count: u.count)
    CTFontGetGlyphsForCharacters(font, &u, &g, u.count)
    var areas: [Double] = []
    var area = 0.0, start = CGPoint.zero, cur = CGPoint.zero
    func edge(_ p: CGPoint) { area += Double(cur.x * p.y - p.x * cur.y) / 2; cur = p }
    if let path = CTFontCreatePathForGlyph(font, g[0], nil) {
        path.applyWithBlock { e in
            let el = e.pointee
            switch el.type {
            case .moveToPoint: area = 0; start = el.points[0]; cur = start
            case .addLineToPoint: edge(el.points[0])
            case .addQuadCurveToPoint: edge(el.points[1])
            case .addCurveToPoint:          // 用控制点折线近似，正负号够用了
                edge(el.points[0]); edge(el.points[1]); edge(el.points[2])
            case .closeSubpath: edge(start); areas.append(area)
            @unknown default: break
            }
        }
    }
    print("\(ch)\t" + areas.map { String(format: "%.0f", $0) }.joined(separator: " "))
}
