import {Box} from "@/app/_components/box";

interface ListProps {
  searched: boolean;
}

export const List = (props: ListProps) => {
  return (
    <Box searched={props.searched}>
      <h1>List</h1>
    </Box>
  );
}