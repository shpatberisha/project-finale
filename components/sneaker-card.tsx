"use client"

import { MoreHorizontal, Edit, Trash2, ExternalLink } from "lucide-react"
import { useState } from "react"

interface Sneaker {
  id: number
  name: string
  brand: string
  price: number
  colorway: string
  releaseYear: number
  categories: string[]
  image: string
}

export function SneakerCard({ sneaker }: { sneaker: Sneaker }) {
  const [showMenu, setShowMenu] = useState(false)

  return (
    <div className="group relative rounded-lg border border-border bg-card overflow-hidden transition-all hover:border-muted-foreground/50">
      <div className="aspect-square bg-secondary relative overflow-hidden">
        <img
          src={sneaker.image}
          alt={sneaker.name}
          className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
          crossOrigin="anonymous"
        />
        <div className="absolute top-3 right-3">
          <div className="relative">
            <button
              onClick={() => setShowMenu(!showMenu)}
              className="rounded-full bg-background/80 backdrop-blur p-1.5 text-foreground opacity-0 group-hover:opacity-100 transition-opacity hover:bg-background"
            >
              <MoreHorizontal className="h-4 w-4" />
            </button>
            {showMenu && (
              <div className="absolute right-0 top-full mt-1 w-36 rounded-md border border-border bg-popover shadow-lg z-10">
                <button className="flex w-full items-center gap-2 px-3 py-2 text-sm text-popover-foreground hover:bg-secondary transition-colors">
                  <Edit className="h-4 w-4" />
                  Edit
                </button>
                <button className="flex w-full items-center gap-2 px-3 py-2 text-sm text-popover-foreground hover:bg-secondary transition-colors">
                  <ExternalLink className="h-4 w-4" />
                  View Details
                </button>
                <button className="flex w-full items-center gap-2 px-3 py-2 text-sm text-destructive hover:bg-secondary transition-colors">
                  <Trash2 className="h-4 w-4" />
                  Delete
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
      <div className="p-4 space-y-2">
        <div className="flex items-start justify-between gap-2">
          <div className="min-w-0">
            <p className="text-xs text-muted-foreground">{sneaker.brand}</p>
            <h3 className="font-medium text-foreground truncate" title={sneaker.name}>
              {sneaker.name}
            </h3>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className="inline-flex items-center rounded-full bg-secondary px-2 py-0.5 text-xs text-muted-foreground">
            {sneaker.colorway}
          </span>
          <span className="inline-flex items-center rounded-full bg-secondary px-2 py-0.5 text-xs text-muted-foreground">
            {sneaker.releaseYear}
          </span>
        </div>
        <div className="flex items-center justify-between pt-2 border-t border-border">
          <span className="text-lg font-semibold text-foreground">${sneaker.price}</span>
          <div className="flex gap-1">
            {sneaker.categories.slice(0, 2).map((category) => (
              <span
                key={category}
                className="text-xs text-muted-foreground"
              >
                {category}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
