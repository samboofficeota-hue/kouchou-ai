import { Button, Field, HStack, Input, Text } from "@chakra-ui/react";
import { ChevronRightIcon } from "lucide-react";
import type { ClusterSettings } from "../types";

export function ClusterSettingsSection({
  clusterLv1,
  clusterLv2,
  recommendedClusters,
  autoAdjusted,
  onLv1Change,
  onLv2Change,
}: {
  clusterLv1: number;
  clusterLv2: number;
  recommendedClusters: ClusterSettings | null;
  autoAdjusted: boolean;
  onLv1Change: (value: number) => void;
  onLv2Change: (value: number) => void;
}) {
  if (!recommendedClusters) return null;

  return (
    <Field.Root mt={4}>
      <Field.Label>意見グループ数設定</Field.Label>
      <HStack w={"100%"}>
        <Button onClick={() => onLv1Change(clusterLv1 - 1)} variant="outline">
          -
        </Button>
        <Input
          type="number"
          value={clusterLv1.toString()}
          min={2}
          max={40}
          onChange={(e) => {
            const v = Number(e.target.value);
            if (!Number.isNaN(v)) {
              onLv1Change(v);
            }
          }}
        />
        <Button onClick={() => onLv1Change(clusterLv1 + 1)} variant="outline">
          +
        </Button>
        <ChevronRightIcon width="100px" />
        <Button onClick={() => onLv2Change(clusterLv2 - 1)} variant="outline">
          -
        </Button>
        <Input
          type="number"
          value={clusterLv2.toString()}
          min={2}
          max={1000}
          onChange={(e) => {
            const inputValue = e.target.value;
            if (inputValue === "") return;
            const v = Number(inputValue);
            if (!Number.isNaN(v)) {
              onLv2Change(v);
            }
          }}
          onBlur={(e) => {
            const v = Number(e.target.value);
            if (!Number.isNaN(v)) {
              onLv2Change(v);
            }
          }}
        />
        <Button onClick={() => onLv2Change(clusterLv2 + 1)} variant="outline">
          +
        </Button>
      </HStack>
      <Field.HelperText>
        階層ごとの意見グループ生成数です。初期値はコメント数に基づいた推奨意見グループ数です。
      </Field.HelperText>
      {autoAdjusted && (
        <Text color="orange.500" fontSize="sm" mt={2}>
          第2階層の意見グループ数が自動調整されました。第2階層の意見グループ数は第1階層の意見グループ数の2倍以上に設定してください。
        </Text>
      )}
    </Field.Root>
  );
}
