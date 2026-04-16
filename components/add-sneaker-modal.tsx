"use client"

import { useState } from "react"
import { X, Loader2 } from "lucide-react"
import useSWR, { useSWRConfig } from "swr"
import { createSneaker, fetcher } from "@/lib/api"
import type { Brand } from "@/lib/types"

interface AddSneakerModalProps {
  isOpen: boolean
  onClose: () => void
}

export function AddSneakerModal({ isOpen, onClose }: AddSneakerModalProps) {
  const [name, setName] = useState("")
  const [brandId, setBrandId] = useState("")
  const [price, setPrice] = useState("")
  const [releaseYear, setReleaseYear] = useState("")
  const [colorway, setColorway] = useState("")
  const [categories, setCategories] = useState("")
  const [productLink, setProductLink] = useState("")
  const [apiKey, setApiKey] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState("")

  const { data: brands } = useSWR<Brand[]>("/api/brands/", fetcher)
  const { mutate } = useSWRConfig()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    
    if (!apiKey) {
      setError("API key is required")
      return
    }

    setIsSubmitting(true)
    try {
      await createSneaker({
        name,
        brand_id: parseInt(brandId),
        price: price ? parseFloat(price) : undefined,
        release_year: releaseYear ? parseInt(releaseYear) : undefined,
        colorway: colorway || undefined,
        categories: categories.split(",").map(c => c.trim()).filter(Boolean),
        product_link: productLink || undefined,
      }, apiKey)
      
      mutate("/api/sneakers/")
      onClose()
      resetForm()
    } catch {
      setError("Failed to create sneaker. Check your API key.")
    } finally {
      setIsSubmitting(false)
    }
  }

  const resetForm = () => {
    setName("")
    setBrandId("")
    setPrice("")
    setReleaseYear("")
    setColorway("")
    setCategories("")
    setProductLink("")
    setApiKey("")
    setError("")
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-background/80 backdrop-blur-sm" onClick={onClose} />
      <div className="relative w-full max-w-md rounded-lg border border-border bg-card p-6 shadow-lg">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-foreground">Add New Sneaker</h2>
          <button
            onClick={onClose}
            className="rounded-full p-1 hover:bg-secondary transition-colors"
          >
            <X className="h-5 w-5 text-muted-foreground" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-foreground mb-1">Name *</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              className="w-full rounded-md border border-border bg-secondary px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
              placeholder="Air Jordan 1 Retro High OG"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-1">Brand *</label>
            <select
              value={brandId}
              onChange={(e) => setBrandId(e.target.value)}
              required
              className="w-full rounded-md border border-border bg-secondary px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
            >
              <option value="">Select a brand</option>
              {brands?.map((brand) => (
                <option key={brand.id} value={brand.id}>
                  {brand.name}
                </option>
              ))}
            </select>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">Price</label>
              <input
                type="number"
                value={price}
                onChange={(e) => setPrice(e.target.value)}
                className="w-full rounded-md border border-border bg-secondary px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
                placeholder="180"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-foreground mb-1">Release Year</label>
              <input
                type="number"
                value={releaseYear}
                onChange={(e) => setReleaseYear(e.target.value)}
                className="w-full rounded-md border border-border bg-secondary px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
                placeholder="2024"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-1">Colorway</label>
            <input
              type="text"
              value={colorway}
              onChange={(e) => setColorway(e.target.value)}
              className="w-full rounded-md border border-border bg-secondary px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
              placeholder="Chicago"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-1">Categories</label>
            <input
              type="text"
              value={categories}
              onChange={(e) => setCategories(e.target.value)}
              className="w-full rounded-md border border-border bg-secondary px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
              placeholder="Basketball, Lifestyle (comma separated)"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-1">Product Link</label>
            <input
              type="url"
              value={productLink}
              onChange={(e) => setProductLink(e.target.value)}
              className="w-full rounded-md border border-border bg-secondary px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
              placeholder="https://nike.com/..."
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground mb-1">API Key *</label>
            <input
              type="password"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              required
              className="w-full rounded-md border border-border bg-secondary px-3 py-2 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
              placeholder="Enter your API key"
            />
          </div>

          {error && (
            <p className="text-sm text-destructive">{error}</p>
          )}

          <div className="flex gap-3 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 rounded-md border border-border px-4 py-2 text-sm font-medium text-foreground hover:bg-secondary transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isSubmitting}
              className="flex-1 flex items-center justify-center gap-2 rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 transition-colors disabled:opacity-50"
            >
              {isSubmitting && <Loader2 className="h-4 w-4 animate-spin" />}
              {isSubmitting ? "Creating..." : "Add Sneaker"}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
