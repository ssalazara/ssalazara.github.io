# 🚀 Storybook Quick Start

**Get your design system running in 2 minutes!**

---

## Step 1: Install (First Time Only)

```bash
npm install
```

**⏱️ Time:** ~2-3 minutes

---

## Step 2: Run Storybook

```bash
npm run dev
```

**⏱️ Time:** ~15 seconds  
**Opens:** `http://localhost:6006`

---

## 🎨 What You'll See

### Foundation
- **Colors** - Blue & gray palette with contrast ratios
- **Typography** - Responsive type scale

### Components
- **Buttons** - 9 variants (primary, secondary, ghost, sizes)
- **Cards** - 5 variants (basic, blog post, grid)
- **Inputs** - 7 variants (text, textarea, validation states)

### Features
- ✅ Interactive controls (change props live)
- ✅ Accessibility testing (WCAG 2.1)
- ✅ Responsive preview (mobile, tablet, desktop)
- ✅ Theme toggle (light/dark backgrounds)

---

## ⌨️ Keyboard Shortcuts

- `⌘/Ctrl + Shift + F` - Search stories
- `⌘/Ctrl + Shift + A` - Toggle addons
- `⌘/Ctrl + Shift + D` - Toggle docs/canvas
- `A` - Toggle accessibility panel

---

## 📝 Useful Commands

```bash
# Run Storybook (default)
npm run storybook

# Compile Sass and run Storybook
npm run dev

# Build static site
npm run build-storybook

# Watch Sass files
npm run sass:watch
```

---

## 🛠️ Quick Tips

### Test Components
1. Click any story (e.g., Button → Primary)
2. Use **Controls** tab to modify props
3. Check **Accessibility** tab for violations
4. Use **Viewport** toolbar to test responsive

### Add New Components
1. Create `stories/components/MyComponent.stories.js`
2. Write story with export default and stories
3. Refresh - auto-detected!

### Change Backgrounds
- Click **background** icon in toolbar
- Switch between light, white, dark

---

## 📚 Full Documentation

- `STORYBOOK-SETUP.md` - Complete setup guide
- `_bmad-output/STORYBOOK-IMPLEMENTATION-COMPLETE.md` - Detailed overview
- `_bmad-output/planning-artifacts/design-system.md` - Design system spec

---

## 🐛 Troubleshooting

**Port in use?**
```bash
npm run storybook -- -p 6007
```

**Sass errors?**
```bash
npm run sass:build
npm run storybook
```

**Stories not showing?**
- Check file naming: `*.stories.js`
- Check location: `stories/` directory
- Restart: `Ctrl+C` then `npm run dev`

---

## ✅ Quick Checklist

- [ ] Run `npm install`
- [ ] Run `npm run dev`
- [ ] Open `http://localhost:6006`
- [ ] Explore **Design System/Introduction**
- [ ] Try **Components/Button** with Controls
- [ ] Check **Accessibility** tab
- [ ] Test **Viewport** toolbar

**Done! You're ready to build! 🎉**

---

**Version:** 1.0  
**Status:** ✅ Ready  
**Last Updated:** 2026-01-19
