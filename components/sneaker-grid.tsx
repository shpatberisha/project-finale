"use client"

import { useState } from "react"
import { SneakerCard } from "./sneaker-card"
import { ChevronDown } from "lucide-react"

const mockSneakers = [
  {
    id: 1,
    name: "Air Jordan 1 Retro High OG",
    brand: "Jordan",
    price: 180,
    colorway: "Chicago",
    releaseYear: 2023,
    categories: ["Basketball", "Lifestyle"],
    image: "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop",
  },
  {
    id: 2,
    name: "Nike Air Max 90",
    brand: "Nike",
    price: 150,
    colorway: "Infrared",
    releaseYear: 2024,
    categories: ["Running", "Lifestyle"],
    image: "https://images.unsplash.com/photo-1600185365926-3a2ce3cdb9eb?w=400&h=400&fit=crop",
  },
  {
    id: 3,
    name: "Nike Dunk Low",
    brand: "Nike",
    price: 110,
    colorway: "Panda",
    releaseYear: 2024,
    categories: ["Skateboarding", "Lifestyle"],
    image: "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=400&h=400&fit=crop",
  },
  {
    id: 4,
    name: "Air Force 1 Low",
    brand: "Nike",
    price: 110,
    colorway: "Triple White",
    releaseYear: 2024,
    categories: ["Basketball", "Lifestyle"],
    image: "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=400&fit=crop",
  },
  {
    id: 5,
    name: "Nike Blazer Mid 77",
    brand: "Nike",
    price: 105,
    colorway: "Vintage White",
    releaseYear: 2023,
    categories: ["Basketball", "Lifestyle"],
    image: "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=400&h=400&fit=crop",
  },
  {
    id: 6,
    name: "Air Jordan 4 Retro",
    brand: "Jordan",
    price: 210,
    colorway: "Bred",
    releaseYear: 2025,
    categories: ["Basketball", "Lifestyle"],
    image: "https://images.unsplash.com/photo-1584735175315-9d5df23860e6?w=400&h=400&fit=crop",
  },
  {
    id: 7,
    name: "Nike React Infinity Run",
    brand: "Nike",
    price: 160,
    colorway: "White Volt",
    releaseYear: 2024,
    categories: ["Running"],
    image: "https://images.unsplash.com/photo-1460353581641-37baddab0fa2?w=400&h=400&fit=crop",
  },
  {
    id: 8,
    name: "Nike Air Max 97",
    brand: "Nike",
    price: 175,
    colorway: "Silver Bullet",
    releaseYear: 2023,
    categories: ["Running", "Lifestyle"],
    image: "https://images.unsplash.com/photo-1605348532760-6753d2c43329?w=400&h=400&fit=crop",
  },
]

export function SneakerGrid() {
  const [sortBy, setSortBy] = useState("newest")

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-foreground">Collection</h1>
          <p className="text-sm text-muted-foreground mt-1">
            {mockSneakers.length} sneakers in your collection
          </p>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-sm text-muted-foreground">Sort by:</span>
          <button className="flex items-center gap-2 rounded-md border border-border bg-secondary px-3 py-2 text-sm text-foreground hover:bg-secondary/80 transition-colors">
            {sortBy === "newest" ? "Newest First" : "Price: Low to High"}
            <ChevronDown className="h-4 w-4" />
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {mockSneakers.map((sneaker) => (
          <SneakerCard key={sneaker.id} sneaker={sneaker} />
        ))}
      </div>
    </div>
  )
}
