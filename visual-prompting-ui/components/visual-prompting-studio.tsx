'use client'

import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Slider } from '@/components/ui/slider'
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Textarea } from '@/components/ui/textarea'
import { ThemeToggle } from '@/components/ui/theme-toggle'
import { Check, Copy, Image as ImageIcon, Loader2, Upload, Video, X } from 'lucide-react'
import { useRef, useState } from 'react'

interface GeneratedPrompt {
  text: string
  mode: string
}

export function VisualPromptingStudio() {
  const [currentMode, setCurrentMode] = useState<'image' | 'video'>('image')
  const [promptType, setPromptType] = useState('standard')
  const [promptText, setPromptText] = useState('')
  const [outputCount, setOutputCount] = useState([1])
  const [selectedImage, setSelectedImage] = useState<File | null>(null)
  const [imagePreview, setImagePreview] = useState<string | null>(null)
  const [isGenerating, setIsGenerating] = useState(false)
  const [generatedPrompts, setGeneratedPrompts] = useState<GeneratedPrompt[]>([])
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setSelectedImage(file)
      const reader = new FileReader()
      reader.onload = (e: ProgressEvent<FileReader>) => {
        setImagePreview(e.target?.result as string)
      }
      reader.readAsDataURL(file)
    }
  }

  const removeImage = () => {
    setSelectedImage(null)
    setImagePreview(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const generatePrompts = async () => {
    // Check if we have either text or image (matching backend validation)
    if (!promptText.trim() && !selectedImage) return

    setIsGenerating(true)

    try {
      let response
      if (selectedImage) {
        // With image
        const formData = new FormData()
        formData.append('mode', currentMode)
        formData.append('num_outputs', outputCount[0].toString())
        formData.append('text_input', promptText)
        formData.append('image', selectedImage)

        response = await fetch('/api/generate-with-image', {
          method: 'POST',
          body: formData
        })
      } else {
        // Without image
        response = await fetch('/api/generate', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            mode: currentMode,
            text_input: promptText,
            num_outputs: outputCount[0]
          })
        })
      }

      if (response.ok) {
        const data = await response.json()
        setGeneratedPrompts(data.prompts.map((text: string) => ({ text, mode: data.mode })))
      } else {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error occurred' }))
        console.error('Generation failed:', errorData.detail || 'Please try again.')
        // You could add a toast notification here
      }
    } catch (error) {
      console.error('Network error occurred. Please check your connection and try again.')
      // You could add a toast notification here
    } finally {
      setIsGenerating(false)
    }
  }

  const copyToClipboard = async (text: string, index: number) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopiedIndex(index)
      setTimeout(() => setCopiedIndex(null), 2000)
    } catch (error) {
      // Fallback for browsers that don't support clipboard API
      const textArea = document.createElement('textarea')
      textArea.value = text
      document.body.appendChild(textArea)
      textArea.select()
      document.execCommand('copy')
      document.body.removeChild(textArea)
      setCopiedIndex(index)
      setTimeout(() => setCopiedIndex(null), 2000)
    }
  }

  return (
    <div className="bg-gradient-to-br from-background to-secondary min-h-screen transition-all duration-300">
      <div className="container mx-auto px-4 py-8">
        {/* Header with theme toggle */}
        <div className="flex justify-between items-center mb-8">
          <div className="text-center flex-1">
            <h1 className="text-4xl font-bold text-foreground mb-2">Visual Prompting Studio</h1>
            <p className="text-muted-foreground text-lg">AI-powered structured prompt generation for visual media</p>
          </div>
          <ThemeToggle />
        </div>

        <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Panel */}
          <Card className="shadow-lg">
            <CardContent className="p-6">
              <div className="mb-6">
                {/* Mode Tabs */}
                <Tabs value={currentMode} onValueChange={(value: string) => setCurrentMode(value as 'image' | 'video')} className="mb-6">
                  <TabsList className="grid w-full grid-cols-2">
                    <TabsTrigger value="image" className="flex items-center">
                      <ImageIcon className="w-4 h-4 mr-2" />
                      Image
                    </TabsTrigger>
                    <TabsTrigger value="video" className="flex items-center">
                      <Video className="w-4 h-4 mr-2" />
                      Video
                    </TabsTrigger>
                  </TabsList>
                </Tabs>

                {/* Prompt Type */}
                <div className="mb-4">
                  <Label htmlFor="promptType">Prompt Type</Label>
                  <Select value={promptType} onValueChange={setPromptType}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select prompt type" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="standard">Standard</SelectItem>
                      <SelectItem value="creative">Creative</SelectItem>
                      <SelectItem value="detailed">Detailed</SelectItem>
                      <SelectItem value="artistic">Artistic</SelectItem>
                      <SelectItem value="photorealistic">Photorealistic</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                {/* Text Input */}
                <div className="mb-4">
                  <Label htmlFor="promptText">Prompt</Label>
                  <Textarea
                    id="promptText"
                    rows={4}
                    value={promptText}
                    onChange={(e) => setPromptText(e.target.value)}
                    placeholder={currentMode === 'image' ? 'Describe what you want to see...' : 'Describe what you want to watch...'}
                  />
                </div>

                {/* Image Upload */}
                <div className="mb-4">
                  <Label className="mb-2 block">Reference Image (Optional)</Label>
                  <div className="flex items-center gap-2">
                    <Button
                      variant="outline"
                      onClick={() => fileInputRef.current?.click()}
                      className="flex items-center"
                    >
                      <Upload className="w-4 h-4 mr-2" />
                      Upload Image
                    </Button>
                    <input
                      ref={fileInputRef}
                      type="file"
                      accept="image/*"
                      onChange={handleImageUpload}
                      className="hidden"
                    />
                  </div>
                  
                  {imagePreview && (
                    <div className="mt-3">
                      <div className="relative w-32 h-32 rounded-md overflow-hidden border">
                        <img src={imagePreview} alt="Preview" className="w-full h-full object-cover" />
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={removeImage}
                          className="absolute top-1 right-1 bg-background/80 hover:bg-background rounded-full p-1 h-auto w-auto"
                        >
                          <X className="w-4 h-4" />
                        </Button>
                      </div>
                    </div>
                  )}
                </div>

                {/* Output Count */}
                <div className="mb-6">
                  <Label className="block mb-4">Number of Outputs: {outputCount[0]}</Label>
                  <Slider
                    value={outputCount}
                    onValueChange={setOutputCount}
                    min={1}
                    max={4}
                    step={1}
                    className="w-full"
                  />
                  <div className="flex justify-between text-xs text-muted-foreground mt-3 px-1">
                    <span>1</span>
                    <span>2</span>
                    <span>3</span>
                    <span>4</span>
                  </div>
                </div>

                {/* Generate Button */}
                <Button
                  onClick={generatePrompts}
                  disabled={(!promptText.trim() && !selectedImage) || isGenerating}
                  className="w-full"
                >
                  {isGenerating ? (
                    <>
                      <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                      Generating...
                    </>
                  ) : (
                    `Generate ${currentMode.charAt(0).toUpperCase() + currentMode.slice(1)} Prompts`
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Results Panel */}
          <Card className="shadow-lg">
            <CardContent className="p-6">
              <h2 className="text-xl font-semibold mb-4">Generated Prompts</h2>
              <div>
                {generatedPrompts.length === 0 ? (
                  <div className="text-center text-muted-foreground py-8">
                    <p className="text-lg mb-2">No prompts generated yet</p>
                    <p className="text-sm">Enter a description and click generate to see your structured prompts</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {generatedPrompts.map((prompt, index) => (
                      <Card key={index} className="border shadow-sm">
                        <CardContent className="p-4">
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-sm font-medium text-muted-foreground capitalize">
                              {prompt.mode} Prompt {generatedPrompts.length > 1 ? `#${index + 1}` : ''}
                            </span>
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => copyToClipboard(prompt.text, index)}
                              className="text-sm"
                            >
                              {copiedIndex === index ? (
                                <>
                                  <Check className="w-4 h-4 mr-1" />
                                  Copied!
                                </>
                              ) : (
                                <>
                                  <Copy className="w-4 h-4 mr-1" />
                                  Copy
                                </>
                              )}
                            </Button>
                          </div>
                          <p className="text-sm text-foreground whitespace-pre-wrap leading-relaxed">
                            {prompt.text}
                          </p>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
} 