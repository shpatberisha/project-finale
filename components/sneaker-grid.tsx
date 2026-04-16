"use client"

import { useState } from "react"
import useSWR from "swr"
import { SneakerCard } from "./sneaker-card"
import { ChevronDown, Loader2 } from "lucide-react"
import { fetcher } from "@/lib/api"
import type { Sneaker, Brand } from "@/lib/types"

const sneakerImages = [
  "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop",
  "https://images.unsplash.com/photo-1600185365926-3a2ce3cdb9eb?w=400&h=400&fit=crop",
  "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=400&h=400&fit=crop",
  "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400&h=400&fit=crop",
  "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=400&h=400&fit=crop",
  "https://images.unsplash.com/photo-1584735175315-9d5df23860e6?w=400&h=400&fit=crop",
  "https://images.unsplash.com/photo-1460353581641-37baddab0fa2?w=400&h=400&fit=crop",
  "https://images.unsplash.com/photo-1605348532760-6753d2c43329?w=400&h=400&fit=crop",
]

export function SneakerGrid() {
  const [sortBy, setSortBy] = useState("newest")
  
  const { data: sneakers, error: sneakersError, isLoading: sneakersLoading } = useSWR<Sneaker[]>(
    "/api/sneakers/",
    fetcher
  )
  
  const { data: brands } = useSWR<Brand[]>("/api/brands/", fetcher)

  const getBrandName = (brandId: number) => {
    const brand = brands?.find((b) => b.id === brandId)
    return brand?.name || "Nike"
  }

  const sortedSneakers = sneakers ? [...sneakers].sort((a, b) => {
    if (sortBy === "newest") {
      return (b.release_year || 0) - (a.release_year || 0)
    } else if (sortBy === "price-low") {
      return (a.price || 0) - (b.price || 0)
    } else if (sortBy === "price-high") {
      return (b.price || 0) - (a.price || 0)
    }
    return 0
  }) : []

  if (sneakersLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
      </div>
    )
  }

  if (sneakersError) {
    return (
      <div className="flex flex-col items-center justify-center h-64 text-center">
        <p className="text-muted-foreground mb-2">Could not connect to the API</p>
        <p className="text-sm text-muted-foreground">
          Make sure your FastAPI server is running at{" "}
          <code className="bg-secondary px-1 rounded">http://localhost:8000</code>
        </p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-foreground">Collection</h1>
          <p className="text-sm text-muted-foreground mt-1">
            {sortedSneakers.length} sneakers in your collection
          </p>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-sm text-muted-foreground">Sort by:</span>
          <button 
            onClick={() => {
              if (sortBy === "newest") setSortBy("price-low")
              else if (sortBy === "price-low") setSortBy("price-high")
              else setSortBy("newest")
            }}
            className="flex items-center gap-2 rounded-md border border-border bg-secondary px-3 py-2 text-sm text-foreground hover:bg-secondary/80 transition-colors"
          >
            {sortBy === "newest" ? "Newest First" : sortBy === "price-low" ? "Price: Low to High" : "Price: High to Low"}
            <ChevronDown className="h-4 w-4" />
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {sortedSneakers.map((sneaker, index) => (
          <SneakerCard 
            key={sneaker.id} 
            sneaker={{
              id: sneaker.id,
              name: sneaker.name,
              brand: getBrandName(sneaker.brand_id),
              price: sneaker.price || 0,
              colorway: sneaker.colorway || "Unknown",
              releaseYear: sneaker.release_year || 2024,
              categories: sneaker.categories,
              image: sneakerImages[index % sneakerImages.length],
            }} 
          />
        ))}
      </div>
    </div>
  )
}
