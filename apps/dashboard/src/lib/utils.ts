/*
 * Copyright (c) 2025 VT Infinite, Inc d/b/a Perswade.xyz
 * Licensed under MIT License (see LICENSE file)
 * Perswade™ - AI-Powered Sales Intelligence Platform
 */

import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
