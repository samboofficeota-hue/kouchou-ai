"use client";

import { getApiBaseUrl } from "@/app/utils/api";
import { Box, Button, Field, Heading, Input, Textarea, VStack } from "@chakra-ui/react";
import { useState } from "react";

export default function SubmitPage() {
  const [slug, setSlug] = useState<string>("");
  const [comment, setComment] = useState<string>("");
  const [source, setSource] = useState<string>("");
  const [url, setUrl] = useState<string>("");
  const [sending, setSending] = useState(false);
  const [done, setDone] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const onSubmit = async () => {
    setError(null);
    setDone(null);
    if (!slug || !comment) {
      setError("ID と コメントは必須です");
      return;
    }
    setSending(true);
    try {
      const res = await fetch(`${getApiBaseUrl()}/submit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ slug, comment, source: source || null, url: url || null }),
      });
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data?.detail || "送信に失敗しました");
      }
      setDone("送信しました。ありがとうございました。");
      setComment("");
    } catch (e: any) {
      setError(e.message);
    } finally {
      setSending(false);
    }
  };

  return (
    <Box mx="auto" maxW="640px" p={8}>
      <Heading size="lg" mb={6}>ご意見の投稿</Heading>
      <VStack gap={4} align="stretch">
        <Field.Root>
          <Field.Label>投稿先ID（レポートID）</Field.Label>
          <Input value={slug} onChange={(e) => setSlug(e.target.value)} placeholder="例: public-opinions" />
        </Field.Root>
        <Field.Root>
          <Field.Label>コメント</Field.Label>
          <Textarea value={comment} onChange={(e) => setComment(e.target.value)} rows={6} placeholder="ご意見を入力してください" />
        </Field.Root>
        <Field.Root>
          <Field.Label>出所（任意）</Field.Label>
          <Input value={source} onChange={(e) => setSource(e.target.value)} placeholder="例: webフォーム" />
        </Field.Root>
        <Field.Root>
          <Field.Label>関連URL（任意）</Field.Label>
          <Input value={url} onChange={(e) => setUrl(e.target.value)} placeholder="https://example.com" />
        </Field.Root>
        <Button onClick={onSubmit} loading={sending} className="gradientBg shadow" w="200px">送信</Button>
        {done && <Box color="green.600">{done}</Box>}
        {error && <Box color="red.600">{error}</Box>}
      </VStack>
    </Box>
  );
}


