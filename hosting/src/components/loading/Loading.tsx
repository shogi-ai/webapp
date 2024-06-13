import "./Loading.css";
interface LoadingProp {
  description: string;
}

export const Loading = ({ description }: LoadingProp) => {
  return (
    <div className="loading">
      <p>{description}</p>
      <div className="spinner"></div>
    </div>
  );
};
