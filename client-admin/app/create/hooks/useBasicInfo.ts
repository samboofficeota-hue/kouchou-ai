import { useState } from "react";
import { v4 } from "uuid";
import { isValidId } from "../utils/validation";

/**
 * 基本情報を管理するカスタムフック
 */
export function useBasicInfo() {
  // 基本情報の状態
  const [input, setInput] = useState<string>(v4());
  const [question, setQuestion] = useState<string>("");
  const [intro, setIntro] = useState<string>("");
  const [isIdValid, setIsIdValid] = useState<boolean>(true);

  /**
   * ID変更時のハンドラー
   */
  const handleIdChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newId = e.target.value;
    setInput(newId);
    setIsIdValid(isValidId(newId));
  };

  /**
   * タイトル変更時のハンドラー
   */
  const handleQuestionChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setQuestion(e.target.value);
  };

  /**
   * 調査概要変更時のハンドラー
   */
  const handleIntroChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setIntro(e.target.value);
  };

  /**
   * 基本情報をリセット
   */
  const resetBasicInfo = () => {
    setInput(v4());
    setQuestion("");
    setIntro("");
    setIsIdValid(true);
  };

  return {
    input,
    question,
    intro,
    isIdValid,
    handleIdChange,
    handleQuestionChange,
    handleIntroChange,
    resetBasicInfo,
  };
}
