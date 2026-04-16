"use client"

import { useState } from "react"

const categories = [
  { name: "All Sneakers", count: 156 },
  { name: "Air Jordan", count: 48 },
  { name: "Air Max", count: 32 },
  { name: "Dunk", count: 28 },
  { name: "Air Force 1", count: 24 },
  { name: "Blazer", count: 12 },
  { name: "React", count: 8 },
  { name: "Free", count: 4 },
]

const brands = [
  { name: "Nike", count: 120 },
  { name: "Jordan", count: 48 },
  { name: "Converse", count: 18 },
]

export function Sidebar() {
  const [activeCategory, setActiveCategory] = useState("All Sneakers")

  return (
    <aside className="hidden lg:block w-64 border-r border-border min-h-[calc(100vh-4rem)] p-6">
      <div className="space-y-6">
        <div>
          <h3 className="text-sm font-medium text-muted-foreground mb-3">Categories</h3>
          <nav className="space-y-1">
            {categories.map((category) => (
              <button
                key={category.name}
                onClick={() => setActiveCategory(category.name)}
                className={`w-full flex items-center justify-between rounded-md px-3 py-2 text-sm transition-colors ${
                  activeCategory === category.name
                    ? "bg-secondary text-foreground"
                    : "text-muted-foreground hover:bg-secondary/50 hover:text-foreground"
                }`}
              >
                <span>{category.name}</span>
                <span className="text-xs text-muted-foreground">{category.count}</span>
              </button>
            ))}
          </nav>
        </div>

        <div className="border-t border-border pt-6">
          <h3 className="text-sm font-medium text-muted-foreground mb-3">Brands</h3>
          <nav className="space-y-1">
            {brands.map((brand) => (
              <button
                key={brand.name}
                className="w-full flex items-center justify-between rounded-md px-3 py-2 text-sm text-muted-foreground hover:bg-secondary/50 hover:text-foreground transition-colors"
              >
                <span>{brand.name}</span>
                <span className="text-xs text-muted-foreground">{brand.count}</span>
              </button>
            ))}
          </nav>
        </div>

        <div className="border-t border-border pt-6">
          <h3 className="text-sm font-medium text-muted-foreground mb-3">Price Range</h3>
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <input
                type="number"
                placeholder="Min"
                className="w-full h-9 rounded-md border border-border bg-secondary px-3 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-ring"
              />
              <span className="text-muted-foreground">-</span>
              <input
                type="number"
                placeholder="Max"
                className="w-full h-9 rounded-md border border-border bg-secondary px-3 text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-ring"
              />
            </div>
          </div>
        </div>

        <div className="border-t border-border pt-6">
          <h3 className="text-sm font-medium text-muted-foreground mb-3">Release Year</h3>
          <select className="w-full h-9 rounded-md border border-border bg-secondary px-3 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-ring">
            <option value="">All Years</option>
            <option value="2026">2026</option>
            <option value="2025">2025</option>
            <option value="2024">2024</option>
            <option value="2023">2023</option>
            <option value="2022">2022</option>
          </select>
        </div>
      </div>
    </aside>
  )
}
