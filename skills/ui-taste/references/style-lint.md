# Style lint

In Tailwind 4, put `--color-*: initial;` in `@theme` before the project
colors, so that only token colors exist. Then add this block to the ESLint config (`eslint.config.mjs` or `.js`), with the paths of
the project:

```js
{
  files: ["src/**/*.{ts,tsx}"],
  ignores: ["src/components/ui/**"],
  rules: {
    "no-restricted-syntax": ["error",
      { selector: "JSXAttribute[name.name='style']", message: "Style through a component in components/ui." },
      { selector: "Literal[value=/#[0-9a-fA-F]{3,8}\\b|rgba?\\(|hsla?\\(|-\\[.+\\]/]", message: "Use a token or a component in components/ui." },
      { selector: "TemplateElement[value.raw=/#[0-9a-fA-F]{3,8}\\b|rgba?\\(|hsla?\\(|-\\[.+\\]/]", message: "Use a token or a component in components/ui." },
    ],
  },
}
```

It blocks the `style` prop, hex, `rgb()` and `hsl()` values, and Tailwind arbitrary values such as
`p-[13px]`.
